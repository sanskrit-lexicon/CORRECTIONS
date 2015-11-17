# NOCHANGE lists
In this subdirectory, I would create no chnage lists.
See https://github.com/sanskrit-lexicon/CORRECTIONS/issues/153 for the details

# Methodology

## Mechanical scraping

### Execution
1. Run `python nochangegenerator.py`

### Logic
`NoChange = WordsExamined - CorrectionsMade.`

`WordsExamined` lists are usually mentioned at the start of corrections issue by the corrector.
Some of the links are not working.
Therefore I am placing them in `testedfiles` folder in this directory.

`CorrectionsMade` is scraped via `nochangegenerator.py` from `[correctionform.txt](https://github.com/sanskrit-lexicon/CORRECTIONS/blob/master/correctionform.txt)`.
### Issues handled via this method
2,8,21,32,36
37 - This corrections submission for AllvsMW.html file went on from issues 37 to 114.


## Manual lists
I will note the manual lists prepared here.

1. [Hiatus list](https://raw.githubusercontent.com/sanskrit-lexicon/MWS/master/hiatus-190-entries.txt) for MW given by Marcis. See Issue 10. It has been processed via nochangegenerator.py and kept as nochange_issue_10.txt.
2. A single correction 'kawunizpAva' in issue 23 added as nochange_issue_23.txt
3. 'bAdarAyaRapu0badaryyA' in 'VCPvsMW.html' and 'VCPvsPW.html' file had one number inside, which spoilt the flow of code. So 'bAdarAyaRa' is written in its place in both the files and processed via mechanical way.

### Issues handled via this method
10,23
