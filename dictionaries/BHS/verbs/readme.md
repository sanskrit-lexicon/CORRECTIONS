Mar 20, 2016
  Headwords of BHS (Buddhist Hybrid Sanskrit) dictionary 
that are verbs (roots) and verb forms
It was noticed that several hundred entries were 3rd singular forms of
verbs, probably mostly prefixed verbs.  The Identification pattern is that
the headword ends in 'ate' or 'ati', which is an uncommon word ending for 
nominal headwords (although words ending in pati, mati, gati are often nouns).

All the headwords are spelled using the SLP1 transliteration.

This analysis depends on two data sources, bhshw2.txt (headwords ) and
bhs.txt (text digitization).  
Note: The redo.sh file assumes that the files of this directory are located at
  bhs/pywork/correctionwork/verbs/.  This script runs the python program
  verbs1.py, which generates several output files.

There are about 17800 items in the current list of headwords 
(bhshw2.txt).

The main task is to find ways to identify the headwords which are verbs.
This task is accomplished by identifying various patterns within the
digitization text for each headword.  Since there is almost no helpful
markup present in bhs.txt,  the program is rather ad hoc.


At this point there are 1266 headwords which are identified as verbs.

One futher distinction is made, whether the headword is a simple root form
 or an inflected form of a root .  For this dictionary, there are NO simple
root forms. (Perhaps the simple root forms appear in the Grammar volume which
accompanies this lexicon.)

These verb forms are typically the third person singular form of a 
root, prefixed root, or some secondary root form (desiderative, causative, etc.).


The headwords (along with accompanying L-number within headwords) are
available in the verbs1.txt (empty in this case) and verbforms1.txt files.

As a potential aid to further study,  an additional file for each of the
two lists is available.  For each headword, there is the text of the
digitization for the headword, as well as a link to the corresponding 
scanned image from the dictionary.

Each of these additional files appears in two formats:
* Emacs org mode (verbs1.org and verbforms1.org)
* Markdown format (verbs1.md and verbforms1.md)



