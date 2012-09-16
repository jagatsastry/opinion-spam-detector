import nltk
import nltk.classify.svm
import svmlight
import pickle


textDir = "/home/jagat/nlp/hotel-reviews"
truthfulRevFile = textDir + "/hotel_truthful"
deceptiveRevFile = textDir + "/hotel_deceptive"

truth = [  nltk.wordpunct_tokenize(line.strip().lower())  for  line   in open(truthfulRevFile) ]
lies = [  nltk.wordpunct_tokenize(line.strip().lower())  for  line   in open(deceptiveRevFile) ]

#print lies

wordHash = {}
idx = 0;
for line in open(truthfulRevFile):
    for word in nltk.wordpunct_tokenize(line.strip().lower()):
      if word not in wordHash:
        idx = idx + 1
        wordHash[word] = idx;

for line in open(deceptiveRevFile):
    for word in nltk.wordpunct_tokenize(line.strip().lower()):
#     print word ,
      if word not in wordHash:
        idx = idx + 1
        wordHash[word] = idx;
#print wordHash.values().sort()
vals = []
for word in wordHash.itervalues():
  vals.append(word)

vals.sort();
print vals

