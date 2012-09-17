#!/bin/bash
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
python pr_recall_fscore.py
