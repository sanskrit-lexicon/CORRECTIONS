April 4, 2016

prep1keys.txt comes from all those records of hwnorm1c.txt 
(a) for which the headword occurs ONLY in CCS, and
(b) Has not already been examined and considered ok  (specifically,
  the headword appears in issue-261/ccsnochange.txt

(hwnorm1c.txt is GitHub/hwnorm1/ejf/hwnorm1c/hwnorm1c.txt)

Construction of prep1keys.txt
(a) ccs-only.txt contains the records of hwnorm1c.txt which have only
    the CCS dictionary  (681 records here)
(b) filter out the records in ccsnochange, and output just the headwords
   (use 2nd field of ccs-only.txt, which contains the CCS spelling of the
    headword; 1st field contains the 'normalized' spelling of headword)
python prep1keys.py ccs-only.txt ../issue-261/ccsnochange.txt prep1keys.txt
80 keys read from ../issue-261/ccsnochange.txt
80 keys dropped from ccs-only.txt
601 keys from ccs-only.txt written to prep1keys.txt

Construction of prep1.org, etc.
python prep1.py ccs prep1keys.txt ../../../orig/ccs.txt ../../ccshw2.txt prep1.org prep1.md

cp prep1.org prep1_edit.org
Now, work through all of prep1_edit.org
