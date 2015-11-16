# NOCHANGE lists
In this subdirectory, I would create no chnage lists.
See https://github.com/sanskrit-lexicon/CORRECTIONS/issues/153 for the details

# Methodology

## Mechanical scraping
### Logic
`NoChange = WordsExamined - CorrectionsMade.`

`WordsExamined` lists are usually mentioned at the start of corrections issue by the corrector.
Some of the links are not working.
Therefore I am placing them in `testedfiles` folder in this directory.

`CorrectionsMade` is scraped via `nochangegenerator.py` from `[correctionform.txt](https://github.com/sanskrit-lexicon/CORRECTIONS/blob/master/correctionform.txt)`.
### Issues handled via this method
2,8,21

## Manual lists
I will note the manual lists prepared here.

1. [Hiatus list](https://raw.githubusercontent.com/sanskrit-lexicon/MWS/master/hiatus-190-entries.txt) for MW given by Marcis. See Issue 10. It has been processed via nochangegenerator.py and kept as nochange_issue_10.txt.
2. A single correction 'kawunizpAva' in issue 23 added as nochange_issue_23.txt

### Issues handled via this method
10,23
