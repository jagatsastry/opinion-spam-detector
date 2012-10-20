import subprocess
from nlp_common import *

def runNestedCV():
    bestCVals = []
    for i in range(NUM_FOLDS):
        bestCVals.append(-1);

    for i in range(NUM_FOLDS):
        cstart = 0
        cmax = 4
        bestAcc = 0

        while int(cstart) <= cmax:
            baseCVals = []
            for j in range(NUM_FOLDS):
                baseCVals.append(cstart);
            predfiles = runSvm(test_review_dir + "/nest_" + str(i), svmdir + "/nest_" + str(i), baseCVals)
    
            curTotAcc = 0
            for predfile in predfiles:
                curTotAcc = curTotAcc + getStats(predfile)[0]
	    avgAcc = float(curTotAcc)/len(predfiles)
	    if avgAcc > bestAcc:
	        bestAcc = avgAcc
	        bestCVals[i] = cstart
        	
	    print "For fold %d, for c value %f, accuracy is %f" % (i, cstart, avgAcc)

	    if cstart < 1:
	        cstart = cstart + 0.1
	    else:
	        cstart = int(cstart) + 1
        

        print "For fold %d, the best c value is %f, with accuracy %f" % (i, bestCVals[i], bestAcc)
    return bestCVals

def runSvm(trdir, outdir, cvals):
    svmexedir = "svmlight"
    testfiles = []
    trainingfiles = []
    modelfiles = []
    predfiles = []
    for i in range(NUM_FOLDS):
        testfiles.append(trdir + "/test_"  + str(i))
        trainingfiles.append(trdir + "/train_" + str(i))
        modelfiles.append(outdir + "/model_" + str(i))
        predfiles.append(outdir + "/pred_" + str(i))
      
    for i in range(NUM_FOLDS):
        print "\n********TRAINING SVM FOR TEST: " + str(i) + "*****************\n"
	params = [svmexedir + "/svm_learn" ] 
	c = cvals[i]
	if c != -1:
	    params = params + ["-c", str(c)]
	params = params + [trainingfiles[i], modelfiles[i]];
        op = subprocess.check_output(params);
        print op
        print "\n********CLASSIFYING TEST CASE: " + str(i) + "**********************\n"
        op2 = subprocess.check_output([svmexedir + "/svm_classify", testfiles[i],  modelfiles[i], predfiles[i]])
        print op2
        print "\n*********END OF TEST 1*************\n"

    return predfiles
  
test_review_dir = "test_review_files"
svmdir = "svm_in_out"

bestCVals = []
for i in range(NUM_FOLDS):
    bestCVals.append(-1);

if CLASSIFIER_TYPE != 'POS':
    print "********RUNNING NESTED VALIDATIONS TO OBTAIN OPTIMUM C*********"
    bestCVals = runNestedCV()
    print "Obtained C values ",bestCVals

print "**********RUNNING CROSS VALIDATIONS**********"
runSvm(test_review_dir, svmdir, bestCVals)
