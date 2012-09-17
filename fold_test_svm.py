import subprocess

trdir = "test_review_files"
svmdir = "svm_in_out"
svmexedir = "svmlight"
testfiles = []
trainingfiles = []
modelfiles = []
predfiles = []
for i in range(5):
    testfiles.append(trdir + "/test_"  + str(i))
    trainingfiles.append(trdir + "/train_" + str(i))
    modelfiles.append(svmdir + "/model_" + str(i))
    predfiles.append(svmdir + "/pred_" + str(i))
  
for i in range(5):
    print "\n********TRAINING SVM FOR TEST: " + str(i) + "*****************\n"
    op = subprocess.check_output([svmexedir + "/svm_learn", "-c", "0", trainingfiles[i], modelfiles[i]])
    print op
    print "\n********CLASSIFYING TEST CASE: " + str(i) + "**********************\n"
    op2 = subprocess.check_output([svmexedir + "/svm_classify", testfiles[i],  modelfiles[i], predfiles[i]])
    print op2
    print "\n*********END OF TEST 1*************\n"
  
