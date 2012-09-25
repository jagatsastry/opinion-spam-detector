import nlp_common
from nlp_common import *
import sys
#print sys.argv

def printFeat(featureSet, label):
    print label,
    for (feat, val) in featureSet:
        print " " + feat + ":" + val,
    print ""


def getWordHashAndDf():
    wordHash = {}
    docFreq = {}
    for line in open("info/Hash_%d_Grams.txt" % (N_IN_NGRAM)):
	toks = line.split(" : ")
	if len(toks) != 3:
	    break
	wordHash[toks[1]] = int(toks[0])
	docFreq[toks[1]] = int(toks[2])
    return [wordHash, docFreq]


externalTestFile = sys.argv[2]
label = sys.argv[3]
hashes = getWordHashAndDf()
wordHash, docFreq = hashes[0], hashes[1]

maxWh = len(wordHash)
for line in open(externalTestFile):
   ngrams = getNGrams(line, N_IN_NGRAM)
   for ng in ngrams:
       if ng not in wordHash:
           wordHash[ng] = maxWh
           maxWh = maxWh + 1  
       if ng not in docFreq:
           docFreq[ng] = 0
       docFreq[ng] = docFreq[ng] + 1

feats = getFeatureVectors(externalTestFile, wordHash, docFreq)
for feat in feats:
    printFeat(feat, label) 


