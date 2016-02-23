First, make two spelling changes in PE, by adding these to manualByLine.txt
24177 old <HI>COURAS. A set of Ks2atriyas who became S4u1dras by
24177 new <HI>CAURAS. A set of Ks2atriyas who became S4u1dras by
; pe, Issue 253, Case 2, User ejf, 02/23/2016
; drAvidas -> drAviqas
31561 old <HI>DRA1VIDAS. It is stated in Maha1bha1rata (Anus4a1sana
31561 new <HI>DRA1VID2AS. It is stated in Maha1bha1rata (Anus4a1sana

Then run:
python updateByLine.py ../orig/pe0.txt manualByLine.txt ../orig/pe.txt

Now, ..

pe_plurals.txt is a list of headwords of PE  that 
(a) end in 's' and
(b) are judged to be cases where
    the final 's' is an English pluralization, and thus should be
    dropped in the 'key1' field. This dropping is done in hw2.py.


possibledisp1.txt is a display, showing the PE text for each of the
  possible plurals:
 python possibledisp1.py pe pe_possible_plurals.txt pe_possible_plurals_disp1.txt
 pe_possible_plurals.txt was from a filter of hwnorm1_v1b.txt of 
  headwords appearing in pe which end in 's' (190 of them).
 The pe_possible_plurals_disp1.txt display was examined to identify those
 in pe_plurals.txt.

pe_plurals.txt is copied up to pywork.
Modifications made to hw2.py to use pe_plurals in determining 'key1'.
update_synch.sh rerun to install these modified key1 cases.
---------------------------------------------------------------------
The rest of the steps update downloads and documentation
step3.  
  remake downloads:
    [cd to downloads dir]
    sh redo_all.sh

prepare new sync update file.
  sh make_sync.sh


step7.  prepare new sanhw1.txt and sanhw2.txt
step7a. On Cologne server, change to scans/awork/sanhw1
  (Assuming still in php/correction_response):
  cd ../../scans/awork/sanhw1/
  sh redo_update.sh
step7b. In local CORRECTIONS repository,
  sh redo_sanhw12.sh

step8. sync with GitHub
step8a. Create commit
step8b. 'Sync'


step9. Make 'installation complete' note in #253.

step10.  Update s3 backup of pe
step10a. Assuming in php/corretion_responses:
  cd  ../../scans/awork/virtualenv/aws/
step10b. Be sure the redo_all.sh of above is finished.
  Make the script, execute it, and deactivate
  python make_copy_environ.py pe
  source s3bk_pe.sh
  rm s3bk_pe.sh

