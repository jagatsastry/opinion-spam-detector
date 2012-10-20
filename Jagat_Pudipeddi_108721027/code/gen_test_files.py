import sys
import os
from nlp_common import *

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

def genFiles(dirName, featureVectorFileName, numRevs):
    testfiles = []
    trainingfiles = []
    for i in range(NUM_FOLDS):
      testfiles.append(open(dirName + "/test_"  + str(i), "w"))
      trainingfiles.append(open(dirName + "/train_" + str(i), "w"))
  
    allRevs = []
    for line in open(featureVectorFileName):
        allRevs.append(line)
    
#    ensure_dir(dirName)

    bucketSize = numRevs/NUM_FOLDS
    for i in range(NUM_FOLDS):
        ll = i * bucketSize
        ul = ll + bucketSize
        tests = allRevs[ll:ul]
        for line in tests:
            testfiles[i].write(line)
        train = allRevs[0:ll] + allRevs[ul:TOT_NUM_DOCS]
        for line in train:
            trainingfiles[i].write(line)        
    
  
mainDir = "test_review_files"
feature_vector_file = sys.argv[2]

genFiles(mainDir, feature_vector_file, TOT_NUM_DOCS)
for i in range(NUM_FOLDS):
    genFiles(mainDir + "/nest_" + str(i), mainDir + "/train_" + str(i), TOT_NUM_DOCS - TOT_NUM_DOCS/NUM_FOLDS)


