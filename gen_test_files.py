from nlp_common import *
trdir = "test_review_files"
testfiles = []
trainingfiles = []
for i in range(NUM_FOLDS):
  testfiles.append(open(trdir + "/test_"  + str(i), "w"))
  trainingfiles.append(open(trdir + "/train_" + str(i), "w"))
  
truth = []
lies = []

i = 0
for line in open("review_features_svm.tfidf"):
    if i/NUM_DOC_PER_LABEL == 0:
        truth.append(line)
    else:
        lies.append(line)
    i = i + 1
ti = 0
li = 0
idx = 0
bucketSize = NUM_DOC_PER_LABEL/NUM_FOLDS
for i in range(NUM_FOLDS):
    ll = i * bucketSize
    ul = ll + bucketSize
    for line in truth[ll:ul] + lies[ll:ul]:
        testfiles[i].write(line)
    for line in (truth[0:ll] + truth[ul:NUM_DOC_PER_LABEL] + lies[0:ll] + lies[ul:NUM_DOC_PER_LABEL]):
        trainingfiles[i].write(line)        
  
