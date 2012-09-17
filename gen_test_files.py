trdir = "test_review_files"
testfiles = []
trainingfiles = []
for i in range(5):
  testfiles.append(open(trdir + "/test_"  + str(i), "w"))
  trainingfiles.append(open(trdir + "/train_" + str(i), "w"))
  
idx = 0
for line in open("review_features_svm.tfidf"):
    flidx = idx / 160
    testfiles[flidx].write(line)
    for i in range(5):
        if i is not flidx:
            trainingfiles[i].write(line)
    idx = idx + 1 
            
  
