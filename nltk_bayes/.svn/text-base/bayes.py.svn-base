import nltk.classify.util
import re
import sys
from nltk.stem.porter import PorterStemmer
from nltk.classify import NaiveBayesClassifier

stopwords = ['i', 'a', 'about', 'an', 'are', 'as', 'at', 'be', 'by', 'for',
        'from', 'how', 'in', 'is', 'it', 'of', 'on', 'or', 'that', 'the',
        'this', 'to', 'was', 'what', 'when', 'where', 'who', 'will', 'with',
        'the', 'its']

stemmer = PorterStemmer()

def read_file(file):
    articles = []
    current = ""
    for line in file:
        if line.strip() == "<!-- BOUNDARY -->":
            articles += [current]
            current = ""
        else:
            current += line
    return articles

def is_stopword(word):
    return word in stopwords

def word_feats(words):
	return dict([(stemmer.stem(word), True) for word in words if word and not is_stopword(word)])

def clean(text):
    text = re.sub('[.,;\'"?!:-]+', '', text)
    text = text.replace('<br />', '')
    text = text.lower()
    text_array = re.split('\s+', text)
    return text_array

# 1 is good 2 is bad
good = read_file(open(sys.argv[1]))
bad = read_file(open(sys.argv[2]))

posfeats = [(word_feats(clean(a)), 'pos') for a in good]
negfeats = [(word_feats(clean(a)), 'neg') for a in bad]

negcutoff = len(negfeats)*3/4
poscutoff = len(posfeats)*3/4

trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
print 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))

classifier = NaiveBayesClassifier.train(trainfeats)
print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
classifier.show_most_informative_features()

dist = classifier.prob_classify(word_feats(a))
print dist.prob('pos')
print dist.prob('neg')


# vi: ts=4 sw=4 sts=0 et:

