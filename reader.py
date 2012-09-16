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
#	  print word ,
	  if word not in wordHash:
	    idx = idx + 1
	    wordHash[word] = idx;
#pickle.dump(wordHash.values().sort(), open("wordhash", "w"));

#pickle.dump(wordHash, open("hash", "w"));
training_data = []
for line in truth[:-100]:
  ufd = nltk.FreqDist(line);
  featureset = [ (wordHash[wordtype], ufd[wordtype]) for wordtype in ufd.keys() ];
  training_data.append((1, featureset));

for line in lies[:-100]:
  ufd = nltk.FreqDist(line);
  featureset = [ (wordHash[wordtype], ufd[wordtype]) for wordtype in ufd.keys() ];
  training_data.append((-1, featureset));

model = svmlight.learn(training_data, 
		type='classification', 
		verbosity=0);
#pickle.dump(model, open("model", "w"));
#model = svmlight.learn(training_data, 
#		type='classification', 
#		verbosity=0);
#model = svmlight.learn([(1, [(120, 2)])], 
#		type='classification', verbosity=0);
#model = svmlight.learn(training_data, type='classification', 
#		verbosity=100.0)

#pickle.dump(model, open("modeldump", "w"));
svmlight.write_model(model, 'my_model.dat')
model = svmlight.read_model('my_model.dat')
test_data = []
for line in truth[-10:]:
  ufd = nltk.FreqDist(line);
  featureset = [ (wordHash[wordtype], ufd[wordtype]) for wordtype in ufd.keys() ];
  test_data.append((0, featureset));

for line in lies[-10:]:
  ufd = nltk.FreqDist(line);
  featureset = [ (wordHash[wordtype], ufd[wordtype]) for wordtype in ufd.keys() ];
  test_data.append((0, featureset));

predictions = []
#svmlight.classify(model, test_data)
lic = 0
trc = 0
for p in predictions:
  if p < 0:
    lic = lic + 1
  else:
    trc = trc + 1
  print '%.8f' % p
print "Lies: "
print lic 
print " Truth: " 
print trc
print len(test_data)

 
