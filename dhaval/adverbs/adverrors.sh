rm -rf adv.txt
rm -rf adv.html

# pwg grep
echo '<?xml version="1.0" encoding="UTF-8"?>' > adv/pwg_adv.xml
echo '<pwg>' >> adv/pwg_adv.xml
grep '<key2>[a-zA-Z]*am</key2></h><body>.*adj.</gram>' ../../../Cologne_localcopy/pwg/pwgxml/xml/pwg.xml >> adv/pwg_adv.xml
echo '</pwg>' >> adv/pwg_adv.xml

# Keeping only the headword:dictcode detail and storing in afem.txt
python adv.py
echo 
echo '##See afem.txt for output##'
echo 
# Linking the digital page and pdf page.
echo "Preparing adv.html with links to webpage and pdf."
python ../tools/link.py adv.txt adv.html Adverbs_marked_as_Adjectives CORRECTIONS 191

