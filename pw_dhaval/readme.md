# Abbreviations of PW
1. Put pw.xml in folder which has abbrv.py. (Not kept because of large size).

2. Run `python abbrv.py` from pywork directory to regenerate the lists.

3. Get the lists in abbrvwork folder.

# Dependencies
[lxml](http://lxml.de/) to parse pw.xml

# Logic
1. `<ls>something</ls>` tag usually holds the literary source data.

2. The text `something` is scraped via lxml and stored in abbrvlist.txt file (1st raw file).

3. abbrvlist.txt file still has some references which are pure numbers. We have discarded them as of now and stored them in purenumberabbrvlist.txt (byproduct). (See https://github.com/sanskrit-lexicon/PWK/issues/11 for details).

4. The list which is not pure numbers, but has some alphabet preceding it is stored in properrefs.txt (raw file 2).

5. The properrefs.txt file still has entries like `TA7N2D2JA-BR.25,13,3.` where the last entries are the canto / shloka number. They need to be removed.

6. The canto or shloka numbers are removed and only unique entries, sorted alphabetically are kept in cleanrefs.txt (raw file 3).

7. Errors usually come solo. Therefore, we have kept a code which sorts cleanrefs based on their occurrences. The actual statistics is stored in stats.txt. Sorted data is stored in sortedcrefs.txt. 

8. After sortedcrefs.txt there is no mechanical handling. It is 3679 entries long file. Check manually and prepare finalabbrv.txt file.

# Improvements in statistics
1. First run - 3679 entries

2. After removing terminal period(.) i.e. `clean = clean.strip('.')` - 3341 entries

