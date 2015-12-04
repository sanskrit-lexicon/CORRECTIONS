echo '::::This is file of previously listed headwords'> output/printed.txt
cd output
shopt -s nullglob
array=(all*.txt)
cd ..
for VALUE in "${array[@]}"
do
	cat "output/"$VALUE >> output/printed.txt
done
python ngram.py $1 $2
