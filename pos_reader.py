from __future__ import division
import nltk
import nltk.classify.svm
import svmlight
import math
from nlp_common import *

def getPosTags(line):
    tagged_words = nltk.pos_tag(nltk.wordpunct_tokenize(line.strip().lower()))
    return [pos for (word, pos) in tagged_words]

  
def getFeatureVectors(filename, ngramHash):
  allFeatures = []
  for line in open(filename):
       ngrams = getPosTags(line, N_IN_NGRAM)
       ufd = nltk.FreqDist(ngrams);
       subHash = {} 
       maxFd = max(ufd.values());
       for ngram in ufd.keys():
           subHash[ngram] = ngramHash[ngram]
       sortedKeys = sorted(subHash, key=lambda key: subHash[key])
       features = []
       for ngramtype in sortedKeys:
           features.append((str(ngramHash[ngramtype]), str((ufd[ngramtype]/maxFd) * math.log(TOT_NUM_DOCS/df[ngramtype]))))
       allFeatures.append(features)
  return allFeatures

textDir = "/home/jagat/nlp/hotel-reviews"
truthfulRevFile = textDir + "/hotel_truthful"
deceptiveRevFile = textDir + "/hotel_deceptive"


ngramHash = {}
df = {}
idx = 0;
truthfulRevs = []
for line in open(truthfulRevFile):
    truthfulRevs.append(line)
    wt = {}
    for ngram in getPosTags(line, N_IN_NGRAM):
      if ngram not in ngramHash:
          idx = idx + 1
          ngramHash[ngram] = idx
      if ngram not in wt:
          if ngram not in df:
              df[ngram] = 1
          else:
              df[ngram] = df[ngram] + 1
          wt[ngram] = True

deceptiveRevs = []
for line in open(deceptiveRevFile):
    deceptiveRevs.append(line)
    wt = {}
    for ngram in getPosTags(line, N_IN_NGRAM):
      if ngram not in ngramHash:
          idx = idx + 1
          ngramHash[ngram] = idx
      if ngram not in wt:
          if ngram not in df:
              df[ngram] = 1
          else:
              df[ngram] = df[ngram] + 1
          wt[ngram] = True


trueFeatures = getFeatureVectors(truthfulRevFile, ngramHash)
deceptiveFeatures = getFeatureVectors(deceptiveRevFile, ngramHash)

for i in range(NUM_DOC_PER_LABEL):
    trueRev = trueFeatures[i]
    print "-1",
    for (feat, val) in trueRev:
        print " " + feat + ":" + val,
    deceptiveRev = deceptiveFeatures[i]
    print ""
    print "+1",
    for (feat, val) in deceptiveRev:
        print " " + feat + ":" + val,
    print ""
    

whfile = open("info/Hash_pos" + str(N_IN_NGRAM) + "_Grams.txt", "w");
srtd = sorted(ngramHash, key=lambda key:  ngramHash[key])
totdf = 0
for key in srtd:
    whfile.write(str(ngramHash[key]) + " : " + key + " : " + str(df[key]) + "\n");
    totdf = totdf + df[key]
whfile.write("Average DF: " + str(totdf/len(df.keys())))
#avg_df =  reduce(lambda x, y: x + y, df.values()) / len(df.values())
#print "Average DF: " + str(avg_df)

