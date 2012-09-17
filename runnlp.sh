#!/bin/bash
ngram=$1
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
tot=0
echo "Accuracies for classication in each fold" 
i=0
for x in `grep Accuracy $opFile | grep -o "[0-9]*\.[0-9]*%" | sed 's/%//g'` 
    do 
	echo "Test $i : $x%"
	tot=`echo "scale=3; $tot + $x" | bc`
	i=`echo "$i + 1" | bc`
    done
avg=`echo "scale=3; $tot / $i" | bc`
echo
echo "Average Accuracy: $avg"

