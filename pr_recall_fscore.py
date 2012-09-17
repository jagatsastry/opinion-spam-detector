from __future__ import division
import math

from math import floor

predFile = open("svm_in_out/pred_0")

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

print "FP: ",fp," TP: ",tp," FN: ",fn," TN: ",tn
precision = tp / (tp + fp)
recall = tp / (tp + fn)
fscore = (2*precision*recall)/(precision + recall)
print "Precision: ",precision
print "Recall: ",recall
print "F-Score: ",fscore






