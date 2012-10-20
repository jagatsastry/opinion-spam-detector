import nlp_common
from nlp_common import *

allStats = []
for i in range(NUM_FOLDS):
    stats = getStats("svm_in_out/pred_" + str(i))
    allStats.append(stats)

printStats(allStats)

