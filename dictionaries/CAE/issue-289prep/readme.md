April 15, 2016

prep1keys.txt comes from all those records of hwnorm1c.txt 
(a) for which the headword occurs ONLY in CAE, and
(b) Has not already been examined and considered ok  

(hwnorm1c.txt is GitHub/hwnorm1/ejf/hwnorm1c/hwnorm1c.txt)

Construction of prep1keys.txt
(a) cae-only.txt contains the records of hwnorm1c.txt which have only
    the CAE dictionary  (874 records here)
(b) filter out the records in caenochange, and output just the headwords
   (use 2nd field of cae-only.txt, which contains the CAE spelling of the
    headword; 1st field contains the 'normalized' spelling of headword)
NOTE: caenochange.txt is empty in this run.
python prep1keys.py cae-only.txt caenochange.txt prep1keys.txt
  0 keys read from ../issue-261/caenochange.txt
  0 keys dropped from cae-only.txt
874 keys from cae-only.txt written to prep1keys.txt


Construction of prep1.org, etc.
python prep1.py cae prep1keys.txt ../../../orig/cae.txt ../../caehw2.txt prep1.org prep1.md

cp prep1.org prep1_edit.org
Now, work through all of prep1_edit.org

When done, construct change-289.txt.
python makechange.py prep1_edit.org change.txt
876 records written to change.txt
p 78
t 251
n 547

change.txt is copied to change-289.txt,
and a couple of alterations are made by hand:
1. anaGaprasavA, marked as no-change, is removed from change-289.txt,
   as it will be entirely deleted separately (see extra.txt)
cae:anaGaprasavA,997:anaGaprasavA:n: Not in dictionary. steganography?
Similarly:
cae:apetASa,2082:apetASa:n:  not in scan. see extra.txt
cae:avagatArTa,3087:avagatArTa:n:  not in text

So, now the number of no change cases is 547-3 = 544.

Now ready for the corrections to be installed at Cologne.
change-289.txt copied to 
scans/awork/correction_templates/hw/changefiles/