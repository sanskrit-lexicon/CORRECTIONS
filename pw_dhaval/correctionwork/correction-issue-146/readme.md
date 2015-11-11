# PW Abbreviations correction

See [this issue](https://github.com/sanskrit-lexicon/CORRECTIONS/issues/147) for the discussion.

##Input -

pywork/abbrvwork/makeabbrv.sh creates many files for abbreviations in PW.

Our input is pywork/abbrvwork/abbrvoutput/finalabbrv.txt in which corrections have been made.

Copy paste it in pywork/correctionwork/correction-issue-146 folder.

## Execution

`python generate.py change.txt ../../../orig/pw.txt ../../pwhw2.txt pwabbrvupd.txt pwabbrvupd.tsv`

## Output -

pwabbrvupd.tsv is the tab separated files

pwabbrvupd.txt is the text file 

## What next -

Append pwabbrvupd.txt at the end of pywork/manualByLine02.txt

`cd to pywork folder`

`python updateByLine.py ../orig/pw2.txt manualByLine02.txt ../orig/pw.txt`

`sh redo_hw.sh`

`sh redo_xml.sh`

This will regenerate pw.xml with corrections.
