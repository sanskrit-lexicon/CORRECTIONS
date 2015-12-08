# pwg grep
echo '<?xml version="1.0" encoding="UTF-8"?>' > pwg_adv.xml
echo '<pwg>' >> pwg_adv.xml
grep '<key2>[a-zA-Z]*am</key2></h><body>.*adj.</gram>' ../../../Cologne_localcopy/pwg/pwgxml/xml/pwg.xml >> adv/pwg_adv.xml
echo '</pwg>' >> pwg_adv.xml
