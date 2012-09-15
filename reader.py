import nltk
import nltk.classify.svm

textDir = "/home/jagat/nlp/hotel-reviews"
truthfulRevFile = textDir + "/hotel_truthful"
deceptiveRevFile = textDir + "/hotel_deceptive"

truth = [  nltk.word_tokenize(line.strip().lower())  for  line   in open(truthfulRevFile) ] 
lies = [  line.strip().lower().split()  for  line   in open(deceptiveRevFile) ] 

print truth[0]

ufd = nltk.FreqDist(truth[0]);

features =  #[ nltk.classify.svm.featurename(word, ufd[word]) for word in set(truth[0]) ]
print features
#print nltk.ngrams( truth[0], 1)
