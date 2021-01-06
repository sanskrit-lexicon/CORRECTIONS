len=(3)
for value in "${len[@]}"
do
	echo "Running abnormending.py"
	python abnormending.py $value 10
	echo "Linking the webpage and PDFs"
	php link.php abnorm_$value.txt abnorm_$value.html Suspect_word_ends 178
done
