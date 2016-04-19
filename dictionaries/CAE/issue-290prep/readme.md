April 18, 2016
--------------------------------------------------------------
Part 1 - not used directly
--------------------------------------------------------------
prep1keys.txt comes from all those records of hwnorm1c.txt 
(a) for which the headword occurs ONLY in both CAE and CCS, and
(b) Has not already been examined and considered ok  

(hwnorm1c.txt is GitHub/hwnorm1/ejf/hwnorm1c/hwnorm1c.txt)

Construction of prep1keys.txt
(a) cae-ccs-only.txt contains the records of hwnorm1c.txt which have only
    the CAE and CCS dictionary  (373 records here)
(b) filter out the records in caenochange, and output just the headwords
   (use 2nd field of cae-ccs-only.txt, which contains the CAE spelling of the
    headword; 1st field contains the 'normalized' spelling of headword)
NOTE: caenochange.txt is empty in this run.
python prep1keys.py cae-ccs-only.txt caenochange.txt prep1keys.txt
  0 keys read from caenochange.txt
  0 keys dropped from cae-only.txt
373 keys from cae-only.txt written to prep1keys.txt


Construction of prep1.org, etc.
python prep1.py cae prep1keys.txt ../../../orig/cae.txt ../../caehw2.txt prep1.org prep1.md

cp prep1.org prep1_edit.org
Now, work through all of prep1_edit.org
--------------------------------------------------------------
Part 2a 
--------------------------------------------------------------
prep1akeys.txt comes from all those records of hwnorm1c.txt 
(a) for which the headword occurs ONLY in both CAE and CCS, and
(b) Has not already been examined and considered ok  
(c) Is not explained by the current analysis of the 'whitelist' program
   (i.e., is not an 'obvious' compound of known words, and a few other similar
    analytical approaches to 'explain' a word in terms of other words.)

Construction of prep1akeys.txt
(a) cae-ccs-onlya.txt contains the records of hwnorm1c.txt which 
    (a1) occur in both the CAE and CCS dictionaries, but in no other dictionary;
and (a2) have eluded programmatic explanation, as indicated in (c) above.

NOTE: caenochange.txt is empty in this run.
python prep1keys.py cae-ccs-onlya.txt caenochange.txt prep1akeys.txt
  0 keys read from caenochange.txt
  0 keys dropped from cae-only.txt
 82 keys from cae-only.txt written to prep1keys.txt


Construction of prep1a.org, etc.
python prep1.py cae prep1akeys.txt ../../../orig/cae.txt ../../caehw2.txt prep1a.org prep1a.md

cp prep1a.org prep1a_edit.org
Now, work through all of prep1a_edit.org
--------------------------------------------------------------
Part 2b
--------------------------------------------------------------

When done, construct change-cae.txt.
python makechange.py prep1a_edit.org change-cae.txt
82 records written to change-cae.txt
p 10
t 13
n 59

-------------------------------------------------------------------
prepare change-ccs.txt  
see ccs/pywork/correctionwork/issue-290prep/readme.md.
-------------------------------------------------------------------
merge change-cae.txt and change-ccs.txt into change-290.txt
cat change-cae.txt change-ccs.txt > change-290.txt
-------------------------------------------------------------------
Add one additional ccs correction for ccs
ccs:kulapa,5014:kutapa:p: alph. order, cf mw,pw

-------------------------------------------------------------------


Now ready for the corrections to be installed at Cologne.
change-290.txt copied to 
scans/awork/correction_templates/hw/changefiles/

