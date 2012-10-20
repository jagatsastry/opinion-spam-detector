#!/bin/bash
N=$1
python external_test.py $N external_review.txt "+1" > feature_vectors/feature_vectors_$N

svmlight/svm_learn feature_vectors/all_fv_"$N"_gram svm_in_out/mega_model_"$N"

svmlight/svm_classify feature_vectors/feature_vectors_$N svm_in_out/mega_model_$N svm_in_out/external_pred_$N

echo "Predictions"
cat svm_in_out/external_pred_$N
