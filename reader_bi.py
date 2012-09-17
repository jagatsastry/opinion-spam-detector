from __future__ import division
import nltk
import nltk.classify.svm
import svmlight
import math
from nlp_common import TOT_NUM_DOCS
from nlp_common import N_IN_NGRAM

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

  
def printSvmIn(filename, label, ngramHash):
  for line in open(filename):
       ngrams = getNGrams(line, N_IN_NGRAM)
       ufd = nltk.FreqDist(ngrams);
       #print "FreqDist: ",ufd
       print label,
       #keys = ufd.keys()
       #keys.sort()
       subHash = {} 
       maxFd = max(ufd.values());
       for ngram in ufd.keys():
           subHash[ngram] = ngramHash[ngram]
       sortedKeys = sorted(subHash, key=lambda key: subHash[key])
       for ngramtype in sortedKeys:
           print " " + str(ngramHash[ngramtype]) + ":" + str((ufd[ngramtype]/maxFd) * math.log(TOT_NUM_DOCS/df[ngramtype])),
         #  print " " + str(ngramHash[ngramtype]) + ":" + str(ufd[ngramtype]),
#       print "#" + str((w, subHash[w]) for w in sortedKeys)
       print ""

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
#          if ngram is "every":
#              print line

#print "ngramHash:",ngramHash
#print "DocFreq:",df

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


printSvmIn(truthfulRevFile, "+1", ngramHash)
printSvmIn(deceptiveRevFile, "-1", ngramHash)

whfile = open("info/Hash_" + str(N_IN_NGRAM) + "_Grams.txt", "w");
srtd = sorted(ngramHash, key=lambda key:  ngramHash[key])
totdf = 0
for key in srtd:
    whfile.write(str(ngramHash[key]) + " : " + key + " : " + str(df[key]) + "\n");
    totdf = totdf + df[key]
whfile.write("Average DF: " + str(totdf/len(df.keys())))
#avg_df =  reduce(lambda x, y: x + y, df.values()) / len(df.values())
#print "Average DF: " + str(avg_df)

