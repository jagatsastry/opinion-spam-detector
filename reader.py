from __future__ import division
import nltk
import math
from nlp_common import *
posTagHash = {}

textDir = "hotel-reviews"
truthfulRevFile = textDir + "/hotel_truthful"
deceptiveRevFile = textDir + "/hotel_deceptive"


ngramHash = {}
df = {}
idx = 0;
truthfulRevs = []
for line in open(truthfulRevFile):
    truthfulRevs.append(line)
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

deceptiveRevs = []
for line in open(deceptiveRevFile):
    deceptiveRevs.append(line)
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


trueFeatures = getFeatureVectors(truthfulRevFile, ngramHash, df)
deceptiveFeatures = getFeatureVectors(deceptiveRevFile, ngramHash, df)

for i in range(int(NUM_DOC_PER_LABEL)):
    trueRev = trueFeatures[i]
    print "-1",
    for (feat, val) in trueRev:
        print " " + feat + ":" + val,
    print ""

    deceptiveRev = deceptiveFeatures[i]
    print "+1",
    for (feat, val) in deceptiveRev:
        print " " + feat + ":" + val,
    print ""
    

whfile = open("info/Hash_" + str(N_IN_NGRAM) + "_Grams.txt", "w");
srtd = sorted(ngramHash, key=lambda key:  ngramHash[key])
totdf = 0
for key in srtd:
    whfile.write(str(ngramHash[key]) + " : " + key + " : " + str(df[key]) + "\n");
    totdf = totdf + df[key]
whfile.write("Average DF: " + str(totdf/len(df.keys())))

if N_IN_NGRAM == 0:
    whfile = open("info/Hash_" + str(N_IN_NGRAM) + "_POS.txt", "w");
    #srtd = sorted(posTagHash, key=lambda key:  posTagHash[key])
    for key in posTagHash:
        whfile.write(key + " : " + str(posTagHash[key]) +  "\n");

#avg_df =  reduce(lambda x, y: x + y, df.values()) / len(df.values())
#print "Average DF: " + str(avg_df)

