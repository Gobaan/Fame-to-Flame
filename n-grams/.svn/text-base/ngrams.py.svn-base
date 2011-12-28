import collections, sys, os, re, math

# make sure the stopwords file is in the same dir as this script
this_dir = os.path.dirname(os.path.abspath(__file__))
stopWords = set(open("%s/stopwords" % this_dir).read().split())

def getSingleWords(text):
    """
    Returns a list of 'words' that should be used for n-gram analysis.
    Arguments:
    - `text`: text to split
    """
    text = re.sub( """['"/-]""", "", text );
    text = re.sub( '[^a-zA-Z ]', " ",  text).lower()

    words = text.split()
    words = [x for x in words if x not in stopWords]
    return words[:-1]


def getWordsForDisplay(text):
    """
    Returns a list of 'words' that should be used for n-gram analysis.
    Arguments:
    - `text`: text to split
    """
    text = re.sub( """['"/-]""", "", text );
    text = re.sub( '[^a-zA-Z ]', " ",  text).lower()
    words = text.split()
    for i in range( 0, len(words) -1 ):
        if not (words[i] in stopWords or len(words[i]) <= 1):
            builder = [words[i]]
            j = i + 1
            while j < len(words) and (words[j] in stopWords or len(words[i]) <= 1):
                builder += [words[j]]
                j = j + 1;
            if j < len(words):
                builder += [words[j]]
            words[i] = tuple(builder)
    words = [x for x in words if not (x in stopWords or len(x) <= 1)]
    return words[:-1]

def main(goodText, badText, getWordsFn):
    """
    Returns a sorted list of [word, strength] pairs for the good text.
    """
    goodWordMap = collections.defaultdict(lambda : 1)
    badWordMap = collections.defaultdict(lambda : 1)
    p = {}
    q = {}
    goodTextWords = getWordsFn(goodText)
    badTextWords = getWordsFn(badText)

    bigram_to_full = {}
    for word_set in goodTextWords:
        full_word = " ".join(word_set)
        bigram = word_set[0] + ' ' + word_set[-1]
        bigram_to_full[bigram] = full_word
        goodWordMap[bigram] = goodWordMap[bigram] + 1;
    for word_set in badTextWords:
        full_word = " ".join(word_set)
        bigram = word_set[0] + ' ' + word_set[-1]
        bigram_to_full[bigram] = full_word
        badWordMap[bigram] = badWordMap[bigram] + 1;
    goodLen = float(len(goodTextWords)) + 1
    badLen = float(len(badTextWords)) + 1
    goodFrequency = collections.defaultdict(lambda : 1. / goodLen)
    badFrequency = collections.defaultdict(lambda : 1. / badLen)
    for word in goodWordMap:
        goodFrequency[word] = float(goodWordMap[word] + 1) / goodLen
    for word in badWordMap:
        badFrequency[word] = float(badWordMap[word] + 1) / badLen

    #Fallback to frequency
    if len(goodTextWords) < 300 or len(badTextWords) < 300:
        print 'stupid'
        bestGood = list(reversed(sorted(goodFrequency.items(), key = lambda x:x[1])))
        bestBad = list(reversed(sorted(badFrequency.items(), key = lambda x:x[1])))
        return (bestGood[:10], bestBad[:10])


    for word in goodWordMap:
        q[word] = goodFrequency[word] * math.log(goodFrequency[word] / badFrequency[word])
    for word in badWordMap:
        p[word] = badFrequency[word] * math.log(badFrequency[word] / goodFrequency[word])

    averageFrequency = len(set(goodTextWords + badTextWords)) / float(goodLen + badLen)

    bestGood = q.items();
    bestGood.sort( key = lambda x:x[1] )
    bestGood.reverse()
    bestGood = [x for x in bestGood if (x[0] not in q or x[0] not in p) or (q[x[0]] > averageFrequency and p[x[0]] > averageFrequency) ]
    bestGood = [[bigram_to_full[bigram[0]]] + [bigram[1]]  for bigram in bestGood]
    bestBad = p.items();
    bestBad.sort( key = lambda x:x[1] )
    bestBad.reverse()
    bestBad = [x for x in bestBad if (x[0] not in q or x[0] not in p) or (q[x[0]] > averageFrequency and p[x[0]] > averageFrequency) ]
    bestBad = [[bigram_to_full[bigram[0]]] + [bigram[1]] for bigram in bestBad]

    return (bestGood[:10], bestBad[:10])

if __name__ == '__main__':
    goodFile = open(sys.argv[1])
    badFile =  open(sys.argv[2])
    good, bad =  main( re.sub("<!-- BOUNDARY -->", "", goodFile.read()),
                              re.sub("<!-- BOUNDARY -->", "", badFile.read()),
			      getWordsForDisplay)
    print good
    print bad

#good - p log (p / q) + q log (q / p)
#p - probability word appears in good side
#q - probablility word appears in bad side

