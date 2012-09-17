from __future__ import division
import math
import nlp_common
from nlp_common import *

from math import floor


def getStats(fold):

    predFile = open("svm_in_out/pred_" + str(fold))
    fn = 0
    fp = 0
    tp = 0
    tn = 0

    idx = 0
    for line in predFile:
        num = int(floor(float(line)))
        if num < 0 and idx < 80:
	    tn = tn + 1
        elif num >= 0 and idx < 80:
            fp = fp + 1
        elif num < 0 and idx >= 80:
            fn = fn + 1
        else:
	    tp = tp + 1
        idx = idx + 1

    #print "FP: ",fp," TP: ",tp," FN: ",fn," TN: ",tn
    accuracy = 100 * (tp + tn)/idx
    precision = 100 * tp / (tp + fp)
    recall = 100 * tp / (tp + fn)
    fscore = (2*precision*recall)/(precision + recall)

    return [accuracy, precision, recall, fscore]


accuracy = 0
precision = 0
recall = 0
fscore = 0

print "\n******Performance Statistics*******\n"
for i in range(NUM_FOLDS):
    stats = getStats(i)
    print "Fold ",i,":",
    print "   Acc: %3.2f%%  P: %3.2f%%  R: %3.2f%% F: %3.2f%%" % (stats[0], stats[1],stats[2],stats[3])
    accuracy = accuracy + stats[0]
    precision = precision + stats[1]
    recall = recall + stats[2]
    fscore = fscore + stats[3]

print
print "--------------------"
print "       Average      "
print "--------------------"
print "   Accuracy:  %3.2f%%" % (accuracy/NUM_FOLDS)
print "   Precision: %3.2f%%" % (precision/NUM_FOLDS)
print "   Recall:    %3.2f%%" % (recall/NUM_FOLDS)
print "   F-Score:   %3.2f%%" % (fscore/NUM_FOLDS)
print "--------------------"   
