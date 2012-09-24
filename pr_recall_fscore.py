from __future__ import division
import math
import nlp_common
from nlp_common import *

from math import floor

accuracy = 0
precision = 0
recall = 0
fscore = 0

negPrecision = 0
negRecall = 0
negFscore = 0

print "\n******Performance Statistics*******\n"
for i in range(NUM_FOLDS):
    stats = getStats("svm_in_out/pred_" + str(i))
    print "Fold ",i,":    Accuracy: %3.2f%%" % (stats[0])
    print "   Deceptive  --  P: %3.2f%%  R: %3.2f%% F: %3.2f%%" % (stats[1], stats[2],stats[3])
    print "   Truth      --  P: %3.2f%%  R: %3.2f%% F: %3.2f%%" % (stats[4], stats[5],stats[6])
    accuracy = accuracy + stats[0]
    precision = precision + stats[1]
    recall = recall + stats[2]
    fscore = fscore + stats[3]
    negPrecision = negPrecision + stats[4]
    negRecall = negRecall + stats[5]
    negFscore = negFscore + stats[6]

print
print "--------------------"
print "       Average      "
print "--------------------"
print "   Accuracy:  %3.2f%%" % (accuracy/NUM_FOLDS)
print "   Precision: Deceptive %3.2f%%  True %3.2f%%" % (precision/NUM_FOLDS, negPrecision/NUM_FOLDS)
print "   Recall:    Deceptive %3.2f%%  True %3.2f%%" % (recall/NUM_FOLDS, negRecall/NUM_FOLDS)
print "   F-Score:   Deceptive %3.2f%%  True %3.2f%%" % (fscore/NUM_FOLDS, negFscore/NUM_FOLDS)
print "--------------------"   
