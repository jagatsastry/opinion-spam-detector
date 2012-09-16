from __future__ import division
import nltk
import nltk.classify.svm
import svmlight
import pickle

def printSvmIn(filename, label):
  for line in open(filename):
       words = nltk.wordpunct_tokenize(line.strip().lower())
       ufd = nltk.FreqDist(words);
       #print "FreqDist: ",ufd
       print label,
       #keys = ufd.keys()
       #keys.sort()
       subHash = {} 
       for word in ufd.keys():
           subHash[word] = wordHash[word]
       sortedKeys = sorted(subHash, key=lambda key: subHash[key])
       for wordtype in sortedKeys:
           print " " + str(wordHash[wordtype]) + ":" + str(800 * ufd[wordtype] / df[wordtype]),
       print ""

textDir = "/home/jagat/nlp/hotel-reviews"
truthfulRevFile = textDir + "/hotel_truthful"
deceptiveRevFile = textDir + "/hotel_deceptive"


wordHash = {}
df = {}
idx = 0;
for line in open(truthfulRevFile):
    wt = {}
    for word in nltk.wordpunct_tokenize(line.strip().lower()):
      if word not in wordHash:
          idx = idx + 1
          wordHash[word] = idx
      if word not in wt:
          if word not in df:
              df[word] = 1
          else:
              df[word] = df[word] + 1
          wt[word] = True

#print "WordHash:",wordHash
#print "DocFreq:",df

for line in open(deceptiveRevFile):
    wordTaken = False
    for word in nltk.wordpunct_tokenize(line.strip().lower()):
      if word not in wordHash:
          idx = idx + 1
          wordHash[word] = idx
      if not wordTaken:
          if word not in df:
              df[word] = 1
          else:
              df[word] = df[word] + 1

printSvmIn(truthfulRevFile, 1)
printSvmIn(deceptiveRevFile, -1)

