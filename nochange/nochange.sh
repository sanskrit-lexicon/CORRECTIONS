echo "#########################"
echo "Running nochangegenerator.py"
echo "#########################"
echo 
#python nochangegenerator.py
echo
echo "#########################"
echo "Generating nc.txt"
echo "#########################"
echo
# See http://stackoverflow.com/questions/10981439/reading-filenames-into-an-array
cd output
shopt -s nullglob
array=(*)
cd ..
rm -rf nc.txt
rm -rf nochange.txt
rm -rf nochange1.txt
rm -rf nochange2.txt
for VALUE in "${array[@]}"
do
	cat "output/"$VALUE >> nc.txt
done
echo 
echo "#########################"
echo "Generating nochange.txt (nc.txt unique entries)"
echo "#########################"
echo
awk '!a[$0]++' nc.txt >> nochange.txt
echo "#########################"
echo "Generating nochange1.txt (nochange.txt with dictionary codes)"
echo "#########################"
echo "Script may take around an hour to execute."
echo "Checke nochange1.txt and see the data size increase"
echo "to see whether the script is running or not."
while read name
do
	grep "^"$name":" ../sanhw1/sanhw1.txt >> nochange1.txt
done < nochange.txt
echo
echo "#########################"
echo "Generating nochange2.txt (nochange.txt with dictionary codes and L numbers)"
echo "#########################"
echo "Script may take around an hour to execute."
echo "Checke nochange2.txt and see the data size increase"
echo "to see whether the script is running or not."
while read name
do
	grep "^"$name":" ../sanhw2/sanhw2.txt >> nochange2.txt
done < nochange.txt
echo 
