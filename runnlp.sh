#!/bin/bash
python reader.py > review_features_svm.tfidf
python gen_test_files.py
python fold_test_svm.py > op
