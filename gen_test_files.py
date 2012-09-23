import sys
feature_vector_file = sys.argv[2]

from nlp_common import *
trdir = "test_review_files"
testfiles = []
trainingfiles = []
for i in range(NUM_FOLDS):
  testfiles.append(open(trdir + "/test_"  + str(i), "w"))
  trainingfiles.append(open(trdir + "/train_" + str(i), "w"))
  
truth = []
lies = []
allRevs = []
i = 0
for line in open(feature_vector_file):
    allRevs.append(line)
    i = i + 1
ti = 0
li = 0
idx = 0
bucketSize = TOT_NUM_DOCS/NUM_FOLDS
for i in range(NUM_FOLDS):
    ll = i * bucketSize
    ul = ll + bucketSize
    for line in allRevs[ll:ul]:
        testfiles[i].write(line)
    for line in allRevs[0:ll] + allRevs[ul:TOT_NUM_DOCS]:
        trainingfiles[i].write(line)        
  
