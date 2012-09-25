#!/bin/bash
#Jagat Sastry P
#9/17/2012
mkdir -p info
mkdir -p feature_vectors
mkdir -p svm_in_out/nest_0 svm_in_out/nest_1 svm_in_out/nest_2 svm_in_out/nest_3 svm_in_out/nest_4 svm_in_out/nest_5

mkdir -p test_review_files/nest_0 test_review_files/nest_1 test_review_files/nest_2 test_review_files/nest_3 test_review_files/nest_4 test_review_files/nest_5

ngram=$1
if [ "$ngram" = "" ] ; then
    ngram=1
fi
fvFile=feature_vectors/all_fv_"$ngram"_gram
echo
printf "Generating $ngram-gram feature vectors for the documents... "
python reader.py $ngram > $fvFile
echo "Success"
echo
printf "Generating test and training feature vectors for cross validation..."
python gen_test_files.py $ngram $fvFile
echo "Success"
echo
opFile=svm_in_out/svmlight_output_"$ngram"_gram
printf "Training Support Vector Machine and classifying the test documents..."
python fold_test_svm.py $ngram > $opFile
echo "Success..."
echo
# Print statistics
python pr_recall_fscore.py
