import sys

NUM_FOLDS=5
TOT_NUM_DOCS=800
NUM_DOC_PER_LABEL = TOT_NUM_DOCS/2
N_IN_NGRAM=1
if len(sys.argv) > 1:
    N_IN_NGRAM = int(sys.argv[1])

