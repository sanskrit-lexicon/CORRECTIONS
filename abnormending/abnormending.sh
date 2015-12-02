echo "Running abnormending.py"
python abnormending.py
echo "Linking the webpage and PDFs"
php link.php abnorm.txt abnorm.html Suspect_word_ends 178
