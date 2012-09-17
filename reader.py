from __future__ import division
import nltk
import nltk.classify.svm
import svmlight
import pickle

def printSvmIn(filename, label, wordHash):
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
           print " " + str(wordHash[wordtype]) + ":" + str(10000*ufd[wordtype] / (len(words) * df[wordtype])),
         #  print " " + str(wordHash[wordtype]) + ":" + str(ufd[wordtype]),
#       print "#" + str((w, subHash[w]) for w in sortedKeys)
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
#          if word is "every":
#              print line

#print "WordHash:",wordHash
#print "DocFreq:",df

for line in open(deceptiveRevFile):
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


printSvmIn(truthfulRevFile, -1, wordHash)
printSvmIn(deceptiveRevFile, 1, wordHash)

whfile = open("WordHash.txt", "w");
srtd = sorted(wordHash, key=lambda key:  wordHash[key])
totdf = 0
for key in srtd:
  whfile.write(str(wordHash[key]) + " : " + key + " : " + str(df[key]) + "\n");
  totdf = totdf + df[key]
whfile.write("Average DF: " + str(totdf/len(df.keys())))
#avg_df =  reduce(lambda x, y: x + y, df.values()) / len(df.values())
#print "Average DF: " + str(avg_df)


