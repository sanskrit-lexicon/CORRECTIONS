python abbrv.py
echo "Converting the Anglicized Sanskrit to IAST"
echo 
python transcoder/as_roman.py abbrvoutput/sortedcrefs.txt abbrvoutput/sortedcrefsiast.txt as roman
echo "Preparing dislpay.html for viewing."
php displayhtml.php
