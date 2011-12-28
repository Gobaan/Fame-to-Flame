import sys
sys.path.append("../n-grams")
import ngrams
import collections
import math

max_len = 35000

def zero(): return 0

w = collections.defaultdict(zero)
done = collections.defaultdict(zero)
cookie = 0;

def goodness(words, testing = False):
    global cookie
    if len(words) > max_len:
       words = words[:max_len]

    cookie += 1
    score = 0
    for b in words:

	if testing:
		print b, w[b]
		
        if done[b] == cookie: continue
        done[b] = cookie
        score += w[b]
    return score

delta = 0.002
def train(words, isSpam):
    global cookie
    if len(words) > max_len: 
       words = words[:max_len]
    p = 1.0 / (1 + math.exp(-goodness(words)))
    cookie += 1
    for b in words:
         if done[b] == cookie: continue   
         done[b] = cookie
         w[b] += (int(isSpam) - p) * delta

#Todo program test

def classify(text, testing = False):
    words = tuple(ngrams.getWordsForAnalysis(text))
    return goodness(words, testing)

import random
def train_on_amazon(goodFilename, badFilename):
    goodFile = open(goodFilename)
    badFile =  open(badFilename)
 
    goodArticles = [inputText for inputText in goodFile.read().split("<!-- BOUNDARY -->")]
    goodArticles.sort()
    #random.shuffle(goodArticles)
    good_index = int(len(goodArticles) * 9.0 / 10.0)
    goodWords = [tuple(ngrams.getWordsForAnalysis(inputText)) 
		 for inputText in goodArticles][:good_index]

    badArticles = [inputText for inputText in badFile.read().split("<!-- BOUNDARY -->")]
    badArticles.sort()
    #random.shuffle(badArticles)
    bad_index = int(len(badArticles) * 9.0 / 10.0)
    badWords = [tuple(ngrams.getWordsForAnalysis(inputText)) 
		for inputText in badArticles][:bad_index]

    for document in goodWords:
        train(document, True)

    for document in badWords:
        train(document, False)
    
    if __name__ == '__main__': 
    	print 'good results'
    	results = [(classify(document), document) for document in goodArticles[good_index:]]
    	percent = ['%s\n%s' % (result, document) for result, document in results if result < 0]
    	print '\n'.join(sorted(percent))
    	print 1.0 * sum([result for result, document in results]) / len(results) 	
    	print 'percent:%s' % ( len(percent) *1.0 / len(results))

    	print 'bad results'
    	results = [(classify(document), document) for document in badArticles[bad_index:]]

    	percent = ['%s\n%s' % (result, document) for result, document in results if result > 0]
    	print '\n'.join(sorted(percent))
    	print 1.0 * sum([result for result, document in results]) / len(results) 	
    	print 'percent:%s' % (1.0 * len(percent) / len(results))

import pickle
if __name__ == '__main__':
    try:
        with open('classification.cache', 'r') as cache:
            w = pickle.load(cache)
    except IOError:   
        train_on_amazon('../sentiment/reviews/cleaned_good', '../sentiment/reviews/cleaned_bad')
	with open('classification.cache', 'w') as cache:
            pickle.dump(w, cache)

    results = [(key, value) for key, value in w.iteritems()]   
    def compare(a, b):
    	n = a[1] - b[1]
        if n == 0: return 0
        if n < 0: return -1
        if n > 0: return 1
                                                             
    results.sort(cmp = compare)
    print results[:10]
    print results[-10:]



    while (True):
       text = raw_input("Please enter text\n")
       if text == "quit": break
       print classify(text, True)
