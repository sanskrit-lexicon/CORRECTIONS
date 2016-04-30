python alphamismatch.py
list=(ACC CAE AE AP90 AP BEN BHS BOP BOR BUR CCS GRA GST IEG INM KRM MCI MD MW72 MW MWE PD PE PGN PUI PWG PW SCH SHS SKD SNP STC VCP VEI WIL YAT)
for Val in "${list[@]}"
do
	python ../tools/link.py 'mismatch/'$Val'mismatch.txt' 'html/'$Val'mismatch.html' $Val'_alphabetic_mismatch' CORRECTIONS 293
done
