#!/bin/bash
ngram=$1
python reader_bi.py $ngram > review_features_svm.tfidf
python gen_test_files.py
python fold_test_svm.py > op$ngram
