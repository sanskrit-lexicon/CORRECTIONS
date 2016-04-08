April 8, 2016

prep1keys.txt comes from all those records of hwnorm1c.txt 
(a) for which the headword occurs ONLY in CCS, and
(b) Has not already been examined and considered ok  

(hwnorm1c.txt is GitHub/hwnorm1/ejf/hwnorm1c/hwnorm1c.txt)

Construction of prep1keys.txt
(a) ccs-only.txt contains the records of hwnorm1c.txt which have only
    the CCS dictionary  (681 records here)
(b) filter out the records in ccsnochange, and output just the headwords
   (use 2nd field of ccs-only.txt, which contains the CCS spelling of the
    headword; 1st field contains the 'normalized' spelling of headword)
cat ../issue-261/ccsnochange.txt ../issue-264/ccsnochange.txt >ccsnochange.txt
python prep1keys.py ccs-only.txt ccsnochange.txt prep1keys.txt
139 keys read from ../issue-261/ccsnochange.txt
139 keys dropped from ccs-only.txt
 9 keys from ccs-only.txt written to prep1keys.txt

Construction of prep1.org, etc.
python prep1.py ccs prep1keys.txt ../../../orig/ccs.txt ../../ccshw2.txt prep1.org prep1.md

cp prep1.org prep1_edit.org
Now, work through all of prep1_edit.org

When done, construct change-265.txt.
python makechange.py prep1_edit.org change-265.txt

Now ready for the corrections to be installed at Cologne.
