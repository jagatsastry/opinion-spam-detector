from __future__ import division
import nltk
import nltk.classify.svm
import svmlight
import math
from nlp_common import *

def getNGrams(line, n):
    if n <= 0:
	return []
    words = nltk.wordpunct_tokenize(line.strip().lower())
    ngrams = nltk.ngrams(words, n)
    ngramArr = []
    for ngram in ngrams:
        ngramStr =  ngram[0]
        for i in range(n-1):
            ngramStr = ngramStr + "##" + ngram[i + 1]
        ngramArr.append(ngramStr)
    
    return ngramArr + getNGrams(line, n - 1) 

  
def getLabeledFeatures(filename, label, ngramHash):
  labeledFeatures = []
  maxDocLen = 0
  ngramsArr = []
  for line in open(filename):
       ngrams = getNGrams(line, N_IN_NGRAM)
       if(len(ngrams) > maxDocLen):
           maxDocLen = len(ngrams)
       ngramsArr.append(ngrams)

  maxMaxFd = 0
  for ngrams in ngramsArr:
       #ngrams = getNGrams(line, N_IN_NGRAM)
       ufd = nltk.FreqDist(ngrams);
       
       features = {}
       subHash = {} 
       for ngram in ufd.keys():
           subHash[ngram] = ngramHash[ngram]
       sortedKeys = sorted(subHash, key=lambda key: subHash[key])
       maxFd = max(ufd.values());
       if(maxMaxFd < maxFd):
           maxMaxFd = maxFd
       for ngramtype in sortedKeys:
           #features[str(ngramHash[ngramtype])] = int( (ufd[ngramtype]/maxFd) * math.log(TOT_NUM_DOCS/df[ngramtype]));
           val = int(ufd[ngramtype] * math.log(TOT_NUM_DOCS/df[ngramtype]));
	   if val != 0:
               features[ngramtype] =  val

       labeledFeatures.append((features, label));

  return labeledFeatures;

textDir = "/home/jagat/nlp/hotel-reviews"
truthfulRevFile = textDir + "/hotel_truthful"
deceptiveRevFile = textDir + "/hotel_deceptive"


ngramHash = {}
df = {}
idx = 0;
for line in open(truthfulRevFile):
    wt = {}
    for ngram in getNGrams(line, N_IN_NGRAM):
      if ngram not in ngramHash:
          idx = idx + 1
          ngramHash[ngram] = idx
      if ngram not in wt:
          if ngram not in df:
              df[ngram] = 1
          else:
              df[ngram] = df[ngram] + 1
          wt[ngram] = True

for line in open(deceptiveRevFile):
    wt = {}
    for ngram in getNGrams(line, N_IN_NGRAM):
      if ngram not in ngramHash:
          idx = idx + 1
          ngramHash[ngram] = idx
      if ngram not in wt:
          if ngram not in df:
              df[ngram] = 1
          else:
              df[ngram] = df[ngram] + 1
          wt[ngram] = True


allFeatures = getLabeledFeatures(truthfulRevFile, "-1", ngramHash) + getLabeledFeatures(deceptiveRevFile, "+1", ngramHash)
truthfulFeatures, deceptiveFeatures = allFeatures[0:400], allFeatures[400:800]

#trainSet, testSet = allFeatures[80:400] + allFeatures[480:800], allFeatures[:80] + allFeatures[400:480]
#trainSet, testSet = allFeatures[0:80] + allFeatures[160:480] + allFeatures[560:800], allFeatures[80:160] + allFeatures[480:560]
trainSet, testSet = [], [] #allFeatures[0:160] + allFeatures[240:560] + allFeatures[640:800], allFeatures[160:240] + allFeatures[560:640]
ti = 0
li = 0
idx = 0
bucketSize = NUM_DOC_PER_LABEL/NUM_FOLDS
sumAcc = 0
for i in range(NUM_FOLDS):
    trainSet, testSet = [], [] #allFeatures[0:160] + allFeatures[240:560] + allFeatures[640:800], allFeatures[160:240] + allFeatures[560:640]
    ll = int(i * bucketSize)
    ul = int(ll + bucketSize)
    for fset in truthfulFeatures[ll:ul] + deceptiveFeatures[ll:ul]:
        testSet.append(fset)
    for fset in (truthfulFeatures[0:ll] + truthfulFeatures[ul:NUM_DOC_PER_LABEL] + deceptiveFeatures[0:ll] + deceptiveFeatures[ul:NUM_DOC_PER_LABEL]):
        trainSet.append(fset)


    classifier = nltk.NaiveBayesClassifier.train(trainSet)
    acc = nltk.classify.accuracy(classifier, testSet)
    print "Accuracy for fold %d" % i ,acc
    sumAcc = sumAcc + acc

print "Average accuracy %f" % (sumAcc/NUM_FOLDS)
whfile = open("info/Hash_" + str(N_IN_NGRAM) + "_Grams.txt", "w");
srtd = sorted(ngramHash, key=lambda key:  ngramHash[key])
totdf = 0
for key in srtd:
    whfile.write(str(ngramHash[key]) + " : " + key + " : " + str(df[key]) + "\n");
    totdf = totdf + df[key]
whfile.write("Average DF: " + str(totdf/len(df.keys())))
#avg_df =  reduce(lambda x, y: x + y, df.values()) / len(df.values())
#print "Average DF: " + str(avg_df)

