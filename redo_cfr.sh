echo "This script needs to be run with GitBash on windows OS"
echo "download new cfr.tsv from Cologne"
curl -o cfr.tsv http://www.sanskrit-lexicon.uni-koeln.de/php/correction_response/cfr.tsv
echo "regenerate correctionform.txt"
python cfr_adj.py cfr.tsv correctionform.txt
echo "redo_cfr.sh is finished"

