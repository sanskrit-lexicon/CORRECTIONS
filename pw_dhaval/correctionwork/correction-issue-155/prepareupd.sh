dictname=(ACC CAE AE AP90 AP BEN BHS BOP BOR BUR CCS GRA GST IEG INM KRM MCI MD MW72 MW MWE PD PE PGN PUI PWG PW SCH SHS SKD SNP STC VCP VEI WIL YAT)
#dictname=(PW)
echo "Removing old upd directory"
rm -rf upd
echo "Created new upd directory"
mkdir upd
#rm upd/allchangeupd.tsv
#rm upd/allchangeupd.txt
#rm upd/allnochange.txt
#rm upd/allnotfound.txt
for VALUE in "${dictname[@]}"
do
	echo "Handling "$VALUE" dictionary"
	python generate.py change.txt ../../../../"$VALUE"/"$VALUE"txt/"$VALUE".txt ../../../../"$VALUE"/"$VALUE"xml/xml/"$VALUE"hw2.txt upd/"$VALUE"abbrvupd.txt upd/"$VALUE"abbrvupd.tsv upd/"$VALUE"nochange.txt $VALUE
	echo 
done