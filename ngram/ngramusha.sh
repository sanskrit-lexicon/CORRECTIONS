nnum=(2 3) #Starting from 2, because 1-gram gives usually 'L','|','x','F','Y' kind of errors, which are not that useful.
list=(MW PW PWG PD MW72 VCP SHS YAT WIL SKD CAE AP ACC AP90 CCS SCH STC MD BUR BHS BEN)
for nnu in "${nnum[@]}"
do
	for Val in "${list[@]}"
	do
		python usha.py 'output/allvs'$Val'_'$nnu.txt 'output/usha/allvs'$Val'_'$nnu.txt
	done
done
