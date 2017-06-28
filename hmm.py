"""
Ok, i've got it, a naive bayesian classifier to identify youtube spam
"""
import collections, string, nltk,enchant
class CommonWord:
    def __init__(self, word, sp, nsp):
        self.word=  word
        self.spam_probability=sp
        self.not_spam_probability = nsp

    # def add_word(self):
def multiply(numbers):
    total = 1
    for x in numbers:
        total *= x
    return total
# print(multiply((8, 2, 3, -1, 7)))

def num_of_patterns(astr,pattern):
    astr, pattern = astr.strip(), pattern.strip()
    if pattern == '': return 0

    ind, count, start_flag = 0,0,0
    while True:
        try:
            if start_flag == 0:
                ind = astr.index(pattern)
                start_flag = 1
            else:
                ind += 1 + astr[ind+1:].index(pattern)
            count += 1
        except:
            break
    return count

word_validator = enchant.Dict("en_US")
data = [x.split(",") for x in open("eminem.csv").read().split("\n")]
# print data
del data[0]
# nltk.download()
#first, we need to collect a set of words that are identifiable as spam
words =[]
invalidChars = set(string.punctuation.replace("_", ""))
invalidChars.add("\\")
_total_spam= 0
_total_not_spam = 0
for comment in data:
    if int(comment[-1]) == 1:
        _total_spam = _total_spam+1
        # _spamcount = _spamcount+1 #just keep track of how many spam comments we've processed
        #now we know its spam so get the words
        # for word in nltk.word_tokenize(comment[-2]):
        #we need to remove the invalid/shit words from the comment
        temporary_words  = []
        #split it, remove the bad ones
        for word in comment[-2].split(" "):
            #make sure that the word does not contain numbers, digits or punctuation and is longer than one character
            if not any(char.isdigit() for char in word) and word != '' and not any(char in invalidChars for char in word) and word_validator.check(word) and len(word) > 1:
                temporary_words.append(word) #add them to our temporary
                # words.append(word.lower())
        s = nltk.pos_tag(temporary_words)

        # new_sentence = ' '.join(temporary_words)
        # s = nltk.word_tokenize(new_sentence)
        # p = nltk.pos_tag(s)
        for word in s:
            if word[1] not in ["EX", "SYM", "TO", "IN", "DT", "PRP", "PRP$","WP","WP$","CC","IN"]:
                words.append(word[0].lower())
        # print
    else:
        _total_not_spam = _total_not_spam+1
        # words.append(comment[-2].split(" "))
# w = [y for y in x for x in words]
counter = collections.Counter(words)
print counter.most_common()
processed_words= []
for spam_word in counter.most_common():
    # there's probably an easier way to do this
    _spamcount = 0
    _notspamcount = 0
    for comment in data:
        if int(comment[-1]) == 0:
            _notspamcount  = _notspamcount + num_of_patterns(comment[-2], spam_word[0])
        else:
            _spamcount = _spamcount+ num_of_patterns(comment[-2], spam_word[0])
    # print "Word: %s %s/%s Spam %s/%s Not Spam" %(spam_word[0], _spamcount, _total_spam, _notspamcount, _total_not_spam)
    processed_words.append(CommonWord(spam_word[0], float(_spamcount)/float(_total_spam), float(_notspamcount)/float(_total_not_spam)))
    # print "Word: %s  Spam: %s Not Spam: %s" %(processed_words[-1].word, processed_words[-1].spam_probability, processed_words[-1].not_spam_probability)
# word_dict = {x.word: x for x in processed_words}
test_comment = "eminiem is the worst, check out my vid http://www.youporn.com/watch/12658043/redhead-teacher-showing-how-a-wet-pussy-should-looks-like/"
not_spam_probabilities =[float(_total_not_spam)/float(len(data))]
spam_probabilities = [float(_total_spam)/float(len(data))]
for word in test_comment.split(" "):
    index = next((i for i, item in enumerate(processed_words) if item.word == word), -1)
    if index  != -1:
        spam_probabilities.append(processed_words[index].not_spam_probability)
    else:
        not_spam_probabilities.append(processed_words[index].spam_probability)

not_spam_probability= multiply(not_spam_probabilities)
spam_probability= multiply(spam_probabilities)
# for n in not_spam_probabilities:
# for i in range(0, len(not_spam_probabilities)-1, step=2):
#   not_spam_probabilities = not_spam_probabilities+(not_spam_probabilities[i]*not_spam_probabilities)
print "Probability of Spam %s " % spam_probability
print "Probability of Not Spam %s" %not_spam_probability
