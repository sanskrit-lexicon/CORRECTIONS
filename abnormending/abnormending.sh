len=(1 2 3)
thr=(2 3 4 5 6 7 8 9 10 20 30 40 50)
for threshold in "${thr[@]}"
do
	for value in "${len[@]}"
	do
		echo "Running abnormending.py"
		python abnormending.py $value $threshold
		echo "Linking the webpage and PDFs"
		php link.php abnorm_"$value"_"$threshold".txt abnorm_"$value"_"$threshold".html Suspect_word_ends 178
	done
done
