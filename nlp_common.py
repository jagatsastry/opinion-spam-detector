from __future__ import division
import nltk
import sys

NUM_FOLDS=5
TOT_NUM_DOCS=800
NUM_DOC_PER_LABEL = int(TOT_NUM_DOCS/2)
N_IN_NGRAM=1
if len(sys.argv) > 1:
    N_IN_NGRAM = int(sys.argv[1])

CLASSIFIER_TYPE = 'NGRAM'
if N_IN_NGRAM == 0:
    CLASSIFIER_TYPE = 'POS'
elif N_IN_NGRAM == -1:
    CLASSIFIER_TYPE = 'NB'

from math import floor


def getStats(predFileName):
    
    predictions = []
    predFile = open(predFileName)
    for line in predFile:
        num = int(floor(float(line)))
	predictions.append(num)
    
    return getStatsArr(predictions)

def getStatsArr(predictions, exp=[]):

    fn = 0
    fp = 0
    tp = 0
    tn = 0

    idx = 0
    alt = False
    if len(exp) == 0:
	alt = True

    for line in predictions:
        num = int(floor(float(line)))
        if num < 0 and ((alt and idx % 2 == 0) or (alt != True and exp[idx] == -1)):
            tn = tn + 1
        elif num >= 0 and ((alt and idx % 2 == 0) or (alt != True and exp[idx] == -1)):
            fp = fp + 1
        elif num < 0 and ((alt and idx % 2 == 1) or (alt != True  and exp[idx] == 1)):
            fn = fn + 1
        else:
            tp = tp + 1
        idx = idx + 1

    return getScores(tn, fn, tp, fp) + [tn, fn, tp, fp]
    
def getScores(tn, fn, tp, fp):
    #print "FP: ",fp," TP: ",tp," FN: ",fn," TN: ",tn
    tot = tn + fn + tp + fp
    accuracy = 100 * (tp + tn)/tot
    precision = 100 * tp / (tp + fp)
    negPrecision = 100 * tn / (tn + fn)
    recall = 100 * tp / (tp + fn)
    negRecall = 100 * tn / (tn + fp)
    fscore = (2*precision*recall)/(precision + recall)
    negFscore = (2*negPrecision*negRecall)/(negPrecision + negRecall)

    return [accuracy, precision, recall, fscore, negPrecision, negRecall, negFscore]



import math
from math import floor

def printStats(allStats):
                    
    accuracy = 0
    precision = 0
    recall = 0
    fscore = 0

    negPrecision = 0
    negRecall = 0
    negFscore = 0

    print "\n******Performance Statistics*******\n"
    
    i = 0

    tn = 0
    fn = 0
    tp = 0
    fp = 0
    for stats in allStats:

        print "Fold ",i,":    Accuracy: %3.2f%%" % (stats[0])
        print "   Deceptive  --  P: %3.2f%%  R: %3.2f%% F: %3.2f%%" % (stats[1], stats[2],stats[3])
        print "   Truth      --  P: %3.2f%%  R: %3.2f%% F: %3.2f%%" % (stats[4], stats[5],stats[6])
	tn = tn + stats[7]
	fn = fn + stats[8]
	tp = tp + stats[9]
	fp = fp + stats[10]

	i = i + 1

    avgStats = getScores(tn, fn, tp, fp)

    print
    print "--------------------"
    print "       Average      "
    print "--------------------"
    print "   Accuracy:  %3.2f%%" % (avgStats[0])
    print "   Precision: Deceptive %3.2f%%  True %3.2f%%" % (avgStats[1], avgStats[4])
    print "   Recall:    Deceptive %3.2f%%  True %3.2f%%" % (avgStats[2], avgStats[5])
    print "   F-Score:   Deceptive %3.2f%%  True %3.2f%%" % (avgStats[3], avgStats[6])
    print "--------------------"   

def getNGrams(line, n):
    words = nltk.wordpunct_tokenize(line.strip().lower())
    if CLASSIFIER_TYPE is "POS":
    #if N_IN_NGRAM == 1:
        tagged_words = nltk.wordpunct_tokenize(line.strip().lower())
        for word in words:
            if word not in posTagHash:
                posTagHash[word] = nltk.pos_tag([word])[0][1]

        return [posTagHash[word] for word in words]

    if n <= 0:
        return []
    ngrams = nltk.ngrams(words, n)
    ngramArr = []
    for ngram in ngrams:
        ngramStr =  ngram[0]
        for i in range(n-1):
            ngramStr = ngramStr + "##" + ngram[i + 1]
        ngramArr.append(ngramStr)

    return ngramArr + getNGrams(line, n - 1)


def getFeatureVectors(filename, ngramHash, docFreq):
  allFeatures = []
  for line in open(filename):
       ngrams = getNGrams(line, N_IN_NGRAM)
       ufd = nltk.FreqDist(ngrams);
       subHash = {}
       maxFd = max(ufd.values());
       for ngram in ufd.keys():
           subHash[ngram] = ngramHash[ngram]
       sortedKeys = sorted(subHash, key=lambda key: subHash[key])
       features = []
       for ngramtype in sortedKeys:
           features.append((str(ngramHash[ngramtype]), str((ufd[ngramtype]/maxFd) * math.log(TOT_NUM_DOCS/docFreq[ngramtype]))))
       allFeatures.append(features)
  return allFeatures
                      
