from __future__ import division
import sys

NUM_FOLDS=5
TOT_NUM_DOCS=800
NUM_DOC_PER_LABEL = int(TOT_NUM_DOCS/2)
N_IN_NGRAM=1
if len(sys.argv) > 1:
    N_IN_NGRAM = int(sys.argv[1])

CLASSIFIER_TYPE = 'NGRAM'
if N_IN_NGRAM == 0:
    CLASSIFIER_TYPE = 'POS'
elif N_IN_NGRAM == -1:
    CLASSIFIER_TYPE = 'NB'

from math import floor


def getStats(predFileName):
    
    predictions = []
    predFile = open(predFileName)
    for line in predFile:
        num = int(floor(float(line)))
	predictions.append(num)
    
    return getStatsArr(predictions)

def getStatsArr(predictions, exp=[]):

    fn = 0
    fp = 0
    tp = 0
    tn = 0

    idx = 0
    alt = False
    if len(exp) == 0:
	alt = True

    for line in predictions:
        num = int(floor(float(line)))
        if num < 0 and ((alt and idx % 2 == 0) or (alt != True and exp[idx] == -1)):
            tn = tn + 1
        elif num >= 0 and ((alt and idx % 2 == 0) or (alt != True and exp[idx] == -1)):
            fp = fp + 1
        elif num < 0 and ((alt and idx % 2 == 1) or (alt != True  and exp[idx] == 1)):
            fn = fn + 1
        else:
            tp = tp + 1
        idx = idx + 1

    #print "FP: ",fp," TP: ",tp," FN: ",fn," TN: ",tn
    accuracy = 100 * (tp + tn)/idx
    precision = 100 * tp / (tp + fp)
    negPrecision = 100 * tn / (tn + fn)
    recall = 100 * tp / (tp + fn)
    negRecall = 100 * tn / (tn + fp)
    fscore = (2*precision*recall)/(precision + recall)
    negFscore = (2*negPrecision*negRecall)/(negPrecision + negRecall)

    return [accuracy, precision, recall, fscore, negPrecision, negRecall, negFscore]
    

import math
from math import floor

def printStats(allStats):
                    
    accuracy = 0
    precision = 0
    recall = 0
    fscore = 0

    negPrecision = 0
    negRecall = 0
    negFscore = 0

    print "\n******Performance Statistics*******\n"
    
    i = 0

    for stats in allStats:

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
	i = i + 1

    print
    print "--------------------"
    print "       Average      "
    print "--------------------"
    print "   Accuracy:  %3.2f%%" % (accuracy/NUM_FOLDS)
    print "   Precision: Deceptive %3.2f%%  True %3.2f%%" % (precision/NUM_FOLDS, negPrecision/NUM_FOLDS)
    print "   Recall:    Deceptive %3.2f%%  True %3.2f%%" % (recall/NUM_FOLDS, negRecall/NUM_FOLDS)
    print "   F-Score:   Deceptive %3.2f%%  True %3.2f%%" % (fscore/NUM_FOLDS, negFscore/NUM_FOLDS)
    print "--------------------"   
