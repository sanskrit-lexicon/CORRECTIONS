echo "This script needs to be run with GitBash on windows OS"
echo "download new sanhw12.zip from Cologne"
curl -o sanhw12.zip https://www.sanskrit-lexicon.uni-koeln.de/scans/awork/sanhw1/sanhw12.zip
echo "unzip sanhw12.zip"
unzip sanhw12.zip
echo "move sanhw1.txt to sanhw1"
mv sanhw1.txt sanhw1/
echo "move sanhw2.txt to sanhw2"
mv sanhw2.txt sanhw2/
echo "remove sanhw12.zip"
rm sanhw12.zip
echo "redo_sanhw12.sh is finished"


