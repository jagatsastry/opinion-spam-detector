import sys

NUM_FOLDS=5
TOT_NUM_DOCS=800
NUM_DOC_PER_LABEL = TOT_NUM_DOCS/2
N_IN_NGRAM=1
if len(sys.argv) > 1:
    N_IN_NGRAM = int(sys.argv[1])

from math import floor


def getStats(predFileName):

    predFile = open(predFileName)
    fn = 0
    fp = 0
    tp = 0
    tn = 0

    idx = 0
    for line in predFile:
        num = int(floor(float(line)))
        if num < 0 and idx % 2 == 0:
            tn = tn + 1
        elif num >= 0 and idx % 2 == 0:
            fp = fp + 1
        elif num < 0 and idx % 2 == 1:
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


