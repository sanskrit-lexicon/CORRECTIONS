Mar 7, 2016
  Headwords of Burnouf dictionary that are verbs (roots) and verb forms

  All the headwords are spelled using the SLP1 transliteration.

This depends on two data sources, burhw2.txt (headwords of Burnouf) and
bur.txt (text digitization of Burnouf).  
Note: The redo.sh file assumes that the files of this directory are located at
  bur/pywork/correctionwork/verbs/.  This script runs the python program
  verbs1.py, which generates several output files.

There are about 19000 items in the current list of headwords for Burnouf 
(burhw2.txt).

The main task is to find ways to identify the headwords which are verbs.
This task is accomplished by identifying various patterns within the
digitization text for each headword.  Since there is almost no helpful
markup present in bur.txt,  the program is rather ad hoc.

For instance, many non-verb headwords can be recognized by the presence of
a gender ('m.', etc.) in the first line of the digitization.  Similarly,
other less frequent abbreviations can exclude other non-verb headwords.
Then, various quite specific patterns appear only in verb headwords.  Finally,
there are various explicit headword exclusions or inclusions which complete
the identification of verbs.

At this point there are 5953 headwords which are identified as verbs.

One futher distinction is made, whether the headword is a simple root form
(1745 of these) or an inflected form of a root (4208 of these).
These verb forms are typically the first person singular form of a 
prefixed root or of some secondary root form (desiderative, causative, etc.).
There are also a few infinitive forms.

The headwords (along with accompanying L-number within Burnouf headwords) are
available in the verbs1.txt and verbforms1.txt files.

As a potential aid to further study,  an additional file for each of the
two lists is available.  For each headword, there is the text of the
digitization for the headword, as well as a link to the corresponding 
scanned image from the dictionary.

Each of these additional files appears in two formats:
* Emacs org mode (verbs1.org and verbforms1.org)
* Markdown format (verbs1.md and verbforms1.md)



