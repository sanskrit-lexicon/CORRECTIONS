# Usage
# ngram.sh (No arguments. It autofetches the arguments for ngram.py)
#["MW","PW","PWG","PD","MW72","VCP","SHS","YAT","WIL","SKD","CAE","AP","ACC","AP90","CCS","SCH","STC","MD","BUR","BHS","BEN","PUI","GRA","INM","BOP","IEG","GST","PE","VEI","MCI","KRM","PGN","SNP"]
# These are the dictionaries' list in descending order of headword numbers.
# Got by dictsortnumber.py. It makes sense to use the ngram.sh in the descending order of n-gram and then descending order of dictionaries.
nnum=(2 3) #Starting from 2, because 1-gram gives usually 'L','|','x','F','Y' kind of errors, which are not that useful.
list=(MW PW PWG PD MW72 VCP SHS WIL SKD CAE AP ACC AP90 CCS SCH STC MD BUR BHS BEN)
for nnu in "${nnum[@]}"
do
	for Val in "${list[@]}"
	do
		echo 'started' $Val $nnu'grams testing'
		echo '::::This is file of previously listed headwords'> output/printed.txt
		cd output
		shopt -s nullglob
		array=(all*.txt)
		cd ..
		for VALUE in "${array[@]}"
		do
			cat "output/"$VALUE >> output/printed.txt
		done
		python ngram.py $Val $nnu
		python link.py 'output/allvs'$Val'_'$nnu.txt 'output/html/allvs'$Val'_'$nnu.html All_vs_$Val'_'$nnu'grams' CORRECTIONS 185
		echo 'completed' $Val $nnu'grams testing'
		echo
	done
done
