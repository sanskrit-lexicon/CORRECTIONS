DICT=(CAE AP90 AP BEN BHS BOP BUR CCS GRA GST IEG INM KRM MCI MD MW72 MW PD PE PGN PUI PWG PW SCH SHS SKD SNP STC VCP VEI WIL YAT)
rm -rf afem.txt
# MW grep
echo '<?xml version="1.0" encoding="UTF-8"?>' > afem/mw_afem.xml
echo '<mw>' >> afem/mw_afem.xml
grep 'a</key1>.*</key2></h><body>[ ]*<lex>f\.</lex>' ../../../../mw/mwxml/xml/mw.xml >> afem/mw_afem.xml
echo '</mw>' >> afem/mw_afem.xml
# PW grep
echo '<?xml version="1.0" encoding="UTF-8"?>' > afem/pw_afem.xml
echo '<pw>' >> afem/pw_afem.xml
grep 'a</key1>.*</key2></h><body><gram n="f">f\.' ../../../../pw/pwxml/xml/pw.xml >> afem/pw_afem.xml
echo '</pw>' >> afem/pw_afem.xml
# AP90 grep
echo '<?xml version="1.0" encoding="UTF-8"?>' > afem/ap90_afem.xml
echo '<ap90>' >> afem/ap90_afem.xml
grep 'a</key2></h><body><i>f\.</i>' ../../../../ap90/ap90xml/xml/ap90.xml >> afem/ap90_afem.xml
echo '</ap90>' >> afem/ap90_afem.xml
# ap grep
echo '<?xml version="1.0" encoding="UTF-8"?>' > afem/ap_afem.xml
echo '<ap>' >> afem/ap_afem.xml
grep 'a</key1>.*<body><s>[a-zA-Z]*</s>[ ]*<i>f.</i>' ../../../../ap/apxml/xml/ap.xml >> afem/ap_afem.xml
echo '</ap>' >> afem/ap_afem.xml
# ben grep
# Seems like I am able to get this via notepad++ regex, but not via grep.
# Added four entries manually to ben_afem.xml
# regex in notepad++ is ' f\. <i>([a-zA-Z0-9]+)a[,.]'
# BHS grep
# No errors found by ' f\. <b>[a-zA-Z°]*a</b>'
# bop grep
echo '<?xml version="1.0" encoding="UTF-8"?>' > afem/bop_afem.xml
echo '<bop>' >> afem/bop_afem.xml
grep 'a</key2></h><body><i>f\.</i>' ../../../../bop/bopxml/xml/bop.xml >> afem/bop_afem.xml
echo '</bop>' >> afem/bop_afem.xml
# bur grep
echo '<?xml version="1.0" encoding="UTF-8"?>' > afem/bur_afem.xml
echo '<bur>' >> afem/bur_afem.xml
grep 'a</i> f. ' ../../../../bur/burxml/xml/bur.xml >> afem/bur_afem.xml
echo '</bur>' >> afem/bur_afem.xml
# cae grep
echo '<?xml version="1.0" encoding="UTF-8"?>' > afem/cae_afem.xml
echo '<cae>' >> afem/cae_afem.xml
grep 'a</s>[ ]*·f\. [^<]' ../../../../cae/caexml/xml/cae.xml >> afem/cae_afem.xml
echo '</cae>' >> afem/cae_afem.xml
# ccs grep
echo '<?xml version="1.0" encoding="UTF-8"?>' > afem/ccs_afem.xml
echo '<ccs>' >> afem/ccs_afem.xml
grep 'a</s>¦  <i>f\.</i> [^<]' ../../../../ccs/ccsxml/xml/ccs.xml >> afem/ccs_afem.xml
echo '</ccs>' >> afem/ccs_afem.xml
# gra grep
echo '<?xml version="1.0" encoding="UTF-8"?>' > afem/gra_afem.xml
echo '<gra>' >> afem/gra_afem.xml
grep 'a,</b>[  ]* f[ .]*' ../../../../gra/graxml/xml/gra.xml >> afem/gra_afem.xml
echo '</gra>' >> afem/gra_afem.xml
# gst grep
# nothing found. 241 occurrences both in 'a</key2></h><body>([a-zA-Z])\.[m. ]*f[.n ]+\(' and 'a</key2></h><body>([a-zA-Z])\.[m. ]*f[.n ]+'.
# That means that there are brackets explaining feminine forms in this dict.
# ieg grep
# Nothing found.
# inm grep
# Nothing found.
# krm grep
# Nothing found.
# mci grep
# Nothing found by 'a</b>  f\.'
# md grep
# Nothing found by 'a, <i>f\.</i>'
# mw72 grep
echo '<?xml version="1.0" encoding="UTF-8"?>' > afem/mw72_afem.xml
echo '<mw72>' >> afem/mw72_afem.xml
grep 'a,</i> f\.' ../../../../mw72/mw72xml/xml/mw72.xml >> afem/mw72_afem.xml
echo '</mw72>' >> afem/mw72_afem.xml
# pd grep
echo '<?xml version="1.0" encoding="UTF-8"?>' > afem/pd_afem.xml
echo '<pd>' >> afem/pd_afem.xml
grep 'a) <i>f.</i>' ../../../../pd/pdxml/xml/pd.xml >> afem/pd_afem.xml
echo '</pd>' >> afem/pd_afem.xml
# pe grep
# Nothing found.
# pgn grep
# Nothing found.
# pui grep
# Nothing found.
# pwg grep
echo '<?xml version="1.0" encoding="UTF-8"?>' > afem/pwg_afem.xml
echo '<pwg>' >> afem/pwg_afem.xml
grep 'a</key1>.*</key2></h><body><gram n="f">f\.</gram> [^<]' ../../../../pwg/pwgxml/xml/pwg.xml >> afem/pwg_afem.xml
echo '</pwg>' >> afem/pwg_afem.xml
# sch grep
echo '<?xml version="1.0" encoding="UTF-8"?>' > afem/sch_afem.xml
echo '<sch>' >> afem/sch_afem.xml
grep 'a</key2></h><body>f\.' ../../../../sch/schxml/xml/sch.xml >> afem/sch_afem.xml
echo '</sch>' >> afem/sch_afem.xml
# shs grep
# Nothing found by 'a</key2></h><body>f\. [^(]'
# skd grep
echo '<?xml version="1.0" encoding="UTF-8"?>' > afem/skd_afem.xml
echo '<skd>' >> afem/skd_afem.xml
grep 'a, strI,' ../../../../skd/skdxml/xml/skd.xml >> afem/skd_afem.xml
echo '</skd>' >> afem/skd_afem.xml
# stc grep
#Nothing found by 'a-</b>  f/.'
# skd grep
echo '<?xml version="1.0" encoding="UTF-8"?>' > afem/skd_afem.xml
echo '<skd>' >> afem/skd_afem.xml
grep 'a, strI,' ../../../../skd/skdxml/xml/skd.xml >> afem/skd_afem.xml
echo '</skd>' >> afem/skd_afem.xml
# vcp grep
echo '<?xml version="1.0" encoding="UTF-8"?>' > afem/vcp_afem.xml
echo '<vcp>' >> afem/vcp_afem.xml
grep 'a@}</s>¦<s> strI0' ../../../../vcp/vcpxml/xml/vcp.xml >> afem/vcp_afem.xml
echo '</vcp>' >> afem/vcp_afem.xml
# wil grep
# Nothing found by 'a</s>¦ f. [^(]'
# yat grep
echo '<?xml version="1.0" encoding="UTF-8"?>' > afem/yat_afem.xml
echo '<yat>' >> afem/yat_afem.xml
grep 'a</s>[)][0-9 .]*<i>f.' ../../../../yat/yatxml/xml/yat.xml >> afem/yat_afem.xml
echo '</yat>' >> afem/yat_afem.xml


# Keeping only the headword:dictcode detail and storing in afem.txt
python afem.py
echo 
echo '##See afem.txt for output##'
echo 
# Linking the digital page and pdf page.
echo "Preparing afem.html with links to webpage and pdf."
php link.php
