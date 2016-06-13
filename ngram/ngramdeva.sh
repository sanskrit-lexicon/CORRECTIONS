nnum=(2 3) #Starting from 2, because 1-gram gives usually 'L','|','x','F','Y' kind of errors, which are not that useful.
list=(MW PW PWG PD MW72 VCP SHS YAT WIL SKD CAE AP ACC AP90 CCS SCH STC MD BUR BHS BEN)
for nnu in "${nnum[@]}"
do
	for Val in "${list[@]}"
	do
		python link.py 'output/allvs'$Val'_'$nnu.txt 'output/html/allvs'$Val'_'$nnu.html All_vs_$Val'_'$nnu'grams' CORRECTIONS 185
	done
done
