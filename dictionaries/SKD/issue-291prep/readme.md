April 20, 2016

prep1keys.txt comes from all those records of hwnorm1c.txt 
(a) for which the headword occurs ONLY in SKD, and
(b) the headword is not currently explained in an automated way
 There are 594 cases currently.

(hwnorm1c.txt is GitHub/hwnorm1/ejf/hwnorm1c/hwnorm1c.txt)

Construction of prep1keys.txt
(a) skd-only.txt constructed by
python filterdict.py output/20160419/graylist.txt output/20160419/skd-only.txt skd

python prep1keys.py skd-only.txt prep1keys.txt
  0 keys read from ../issue-261/skdnochange.txt
  0 keys dropped from skd-only.txt
874 keys from skd-only.txt written to prep1keys.txt


Construction of prep1.org, etc.
python prep1.py skd prep1keys.txt ../../../orig/skd.txt ../../skdhw2.txt prep1.org prep1.md

cp prep1.org prep1_edit.org
Now, work through all of prep1_edit.org

When done, construct change-291.txt.
python makechange.py prep1_edit.org change-291.txt prep1_edit_query.org
0334 WARNING: no changes
0526 WARNING: no changes
0529 WARNING: no changes
597 cases initialized
skipping case 0334 * TODOx Case 0334: muktiMdatte [[http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=skd&page=2-468][page 2-468]]
skipping case 0526 * TODOx Case 0526: saBarA [[http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=skd&page=2-478][page 2-478]]
skipping case 0529 * TODOx Case 0529: samBUtamAtre [[http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=skd&page=5-212][page 5-212]]
518 records written to change-291.txt
76 full records written to prep1_edit_query.org
DEVA-p 84
DEVA-? 76
DEVA-n 325
DEVA-t 109


Now ready for the corrections to be installed at Cologne.
change-291.txt copied to 
scans/awork/correction_templates/hw/changefiles/
which creates pywork/correctionwork/issue-291/
for correction installation.
