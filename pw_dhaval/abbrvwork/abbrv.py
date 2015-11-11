#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
from lxml import etree # lxml.de
import re
import codecs
import datetime

"""
# Abbreviations of PW
Run `makeabbrv.sh` from pywork/abbrvwork directory to regenerate the lists.

# Dependencies
[lxml](http://lxml.de/) to parse pw.xml

# Logic
1. `<ls>something</ls>` tag usually holds the literary source data.

2. Output of all scripts are stored in abbrvoutput folder.

3. The text `something` is scraped via lxml and stored in abbrvlist.txt file (1st raw file).

4. abbrvlist.txt file still has some references which are pure numbers. We have discarded them as of now and stored them in purenumberabbrvlist.txt (byproduct). (See https://github.com/sanskrit-lexicon/PWK/issues/11 for details).

5. The list which is not pure numbers, but has some alphabet preceding it is stored in properrefs.txt (raw file 2).

6. The properrefs.txt file still has entries like `TA7N2D2JA-BR.25,13,3.` where the last entries are the canto / shloka number. They need to be removed.

7. The canto or shloka numbers are removed and only unique entries, sorted alphabetically are kept in cleanrefs.txt (raw file 3).

8. Errors usually come solo. Therefore, we have kept a code which sorts cleanrefs based on their occurrences. Sorted data is stored in sortedcrefs.txt. Sorting is done first based on number of occurrences and then alphabetically.

9. sortedcrefs.txt has the data is `ls@key1@key2@Lnumber@occurrence`.

10. It is difficult to read the `ls`, because it is in Anglisized Sanskrit. Therefore we add another field `lsinIAST@ls@key1@key2@Lnumber@occurrence` in  sortedcrefsiast.txt via `transcoder/as_roman.py` file.

11. The file `displayhtml.php` takes sortedcrefsiast.txt as input and gives the following output `SrNo-Lno-ReferenceinAS-ReferenceinIASTwithlinktowebpage-key1withlinktopdf-key2-counter`.

12. This file displayhtml.php would make it easy to locate the reference in dictionaries.

13. For corrections, copy the file `sortedcrefs.txt` as `finalabbrv.txt`. (This is not automated, because otherwise it may be overwritten if handled recklessly).

14. If there are errors found in HTML file, correct the `referenceinAS` in the finalabbrv.txt file.

15. If there is no error, place a ';' before the line in finalabbrv.txt.

16. Once the testing is over, run `python postprocess.py`. It would separate the file into change.txt and nochange.txt.

17. Jim would have to find a way to integrate these files into XML corrections.


# Improvements in statistics
1. First run - 3679 entries

2. After removing terminal period(.) i.e. `clean = clean.strip('.')` - 3341 entries
"""

# Function to return timestamp
def printtimestamp():
	return datetime.datetime.now()
print "Parsing started at", printtimestamp()
print
entries = etree.parse('../pw.xml') # Parse xml
print "Parsing ended at", printtimestamp()
print

# Argument abbrvtag is the tag which contains literary resources data in the given XML file. 
# For PW, it is 'ls'.
def scrapeabbrv(abbrvtag):
	global entries # Fetched parse XML.
	g = codecs.open('abbrvoutput/abbrvlist.txt', 'w','utf-8') # Opened file to store
	pw = entries.xpath('/pw/H1/body/'+abbrvtag) # Scraped only elements in XML tree which have the abbrvtag.
	wholeabbrvlist = []
	for pws in pw:
		abbrvtext = pws.text
		key1 = pws.getparent().getparent().find('h/key1').text.strip()
		key2 = pws.getparent().getparent().find('h/key2').text.strip()
		lnum = pws.getparent().getparent().find('tail/L').text.strip()
		wholeabbrvlist.append((abbrvtext,key1,key2,lnum))
	for (a,b,c,d) in wholeabbrvlist:
		if a is None:
			a = "" # A patch to overcome errors in windows for Nonetype.
		g.write(a+"@"+b+"@"+c+"@"+d+"\n") # Store one in a line in the storage file.
	g.close()
	return wholeabbrvlist # Also return a list.
print "Started scraping the abbreviations from pw.xml at ", printtimestamp()
print
# Change the abbrvtag with suitable tag if you want to extend the code for other dictionaries.
wholeabbrvlist = scrapeabbrv("ls")
print "Stored abbreviations in abbrvoutput/abbrvilst.txt at ", printtimestamp()
print

def segregatepurenumbers():
	global wholeabbrvlist # Fetched global.
	n = codecs.open('abbrvoutput/purenumberabbrvlist.txt','w','utf-8') # n for numbers
	propfile = codecs.open('abbrvoutput/properrefs.txt','w','utf-8') # a for abbreviations (which we are interested in).
	properrefs = []
	for (a,b,c,d) in wholeabbrvlist:
		if a is None:
			a = ""
		if re.match(r'^([^a-zA-Z]*)$',a): # Removing improper reference tags.
			n.write(a+"@"+b+"@"+c+"@"+d+"\n") # Store one in a line in the storage file.
		elif re.match(r'^([0-9a-z()&.,]+)$',a): # Same
			n.write(a+"@"+b+"@"+c+"@"+d+"\n") # Store one in a line in the storage file.
		else:
			propfile.write(a+"@"+b+"@"+c+"@"+d+"\n") # Store one in a line in the storage file.
			properrefs.append((a,b,c,d)) # Append to the list
	propfile.close()
	return properrefs # Return list

print "Segretating references with only numbers to abbrvoutput/purenumberabbrvlist.txt and "
print "proper references to abbrvoutput/properrefs.txt at", printtimestamp()
print
properrefs = segregatepurenumbers()
print "Completed segretating references at ", printtimestamp()
print

def removenumbers():
	global properrefs
	cleanfile = codecs.open('abbrvoutput/cleanrefs.txt','w','utf-8')
	cleanrefs = []
	for (a,b,c,d) in properrefs:
		clean = re.sub(u'¨',u'$',a) # Some unicode issues sorted. Not converted them back as of now.
		clean = re.sub(u'›',u'$$',clean)
		clean = re.sub(u'ý',u'^2',clean)
		clean = re.sub(r'[.]([0-9,.a-z();\^\$]+)$','',clean) # Removed the trailing numbers of cantos / shlokas etc.
		clean = clean.strip('.') # Removed trailing period after the numbers are removed (if any).
		cleanrefs.append((clean,b,c,d))
	cl1 = []
	ur1 = []
	for (p,q,r,s) in cleanrefs:
		if p not in ur1:
			cl1.append((p,q,r,s))
			ur1.append(p)
	uniquerefs = ur1 # Return only the unique references.
	uniquerefs.sort() # Sort alphabetically.
	for i in xrange(len(cl1)):
		cleanfile.write(cl1[i][0]+"@"+cl1[i][1]+"@"+cl1[i][2]+"@"+cl1[i][3]+"\n") # Write to cleanrefs.txt
	cleanfile.close()
	return (uniquerefs, cleanrefs) # Return a tuple with uniquerefs and cleanrefs as members. Both have their utility.
	
print "Removing numbers from properrefs and storing only names of works to abbrvoutput/cleanrefs.txt at ", printtimestamp()
print
(uniquerefs, cleanrefs) = removenumbers()
print "Completed storing clean references at ", printtimestamp()
print
		
def occurrence():
	global cleanrefs, uniquerefs # Fetched from global
	abbstats = codecs.open('abbrvoutput/sortedcrefs.txt','w','utf-8') # Sorted according to occurrences first and alphabetically second.
	occurlist = []
	onlyls = [a for (a,b,c,d) in cleanrefs]
	uniquerefs.sort()
	ur1 = uniquerefs[:]
	for (a,b,c,d) in cleanrefs:
		if a in ur1:
			count = onlyls.count(a)
			occurlist.append((a,b,c,d,count))
			ur1.remove(a)
	occurlist.sort(key=lambda x: (x[4],x[0]))
	for (a,b,c,d,e) in occurlist:
		abbstats.write(a+"@"+b+"@"+c+"@"+d+"@"+str(e)+"\n")
	abbstats.close()
	

print "Sorting the cleanrefs based on occurrences in pw.xml, and storing in sortedcrefs.txt"
print
print "This may take around 1 minute. Please be patient."
print
occurrence()
print "Execution ended at", printtimestamp()
print 
print "Total ", len(uniquerefs), "unique references"
print 
