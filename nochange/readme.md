# NOCHANGE lists
In this subdirectory, I would create no change lists.
See https://github.com/sanskrit-lexicon/CORRECTIONS/issues/153 for the details

# Methodology

## Mechanical scraping

### Execution
1. Run `nochange.sh`

### Where is the input ?
1. All files inside `testedfiles` folder
2. ../sanhw1/sanhw1.txt
3. ../sanhw2/sanhw2.txt

### Where is the output ?
1. `output` folder has files in format `nc_issuenumber.txt` e.g. nc_2.txt for CORRECTIONS issue number 2.
2. `nc.txt` file has all the entries of output folder clubbed together.
3. `nochange.txt` is 'nc.txt' file with duplicate entries removed.
4. `nochange1.txt` is 'nochange.txt' with DictionaryCodes added.
5. `nochange2.txt` is 'nochange.txt' with DictionaryCodes and L numbers added.

### Logic
`NoChange = WordsExamined - CorrectionsMade.`

`WordsExamined` lists are usually mentioned at the start of corrections issue by the corrector.
Some of the links are not working.
Therefore I am placing them in `testedfiles` folder in this directory.

`CorrectionsMade` is scraped via `nochangegenerator.py` from `[correctionform.txt](https://github.com/sanskrit-lexicon/CORRECTIONS/blob/master/correctionform.txt)`.
### Issues handled via this method
2,8,10,21,

32,36,37,38,39,40,47,48,49,50,

51,58,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,

76,77,78,79,80,81,82,83,84,85,88,89,95,98,

101,103,104,106,109,110,111,112,113

Notes :
10 - [Hiatus list](https://raw.githubusercontent.com/sanskrit-lexicon/MWS/master/hiatus-190-entries.txt) for MW given by Marcis. See Issue 10. It has been processed via nochangegenerator.py and kept as nochange_issue_10.txt.

37 - This corrections submission for AllvsMW.html file went on from issues 37 to 114.

60 - The correction submission based on wiltab/compare2.txt file spans over 60,61,62. Treated simultaneously.

63 - Extends from 63 to 67.

## Manual lists
I will note the manual lists prepared here.

1. A single correction 'kawunizpAva'. Right now I have not included it.
2. 'bAdarAyaRapu0badaryyA' in 'VCPvsMW.html' and 'VCPvsPW.html' file had one number inside, which spoilt the flow of code. So 'bAdarAyaRa' is written in its place in both the files and processed via mechanical way.

### Issues handled via this method
23
