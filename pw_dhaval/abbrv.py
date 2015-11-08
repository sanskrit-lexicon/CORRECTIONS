#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
from lxml import etree # lxml.de
import re
import codecs
import datetime

"""
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
"""

# Function to return timestamp
def printtimestamp():
	return datetime.datetime.now()
print "Parsing started at", printtimestamp()
print
entries = etree.parse('pw.xml') # Parse xml
print "Parsing ended at", printtimestamp()
print

# Argument abbrvtag is the tag which contains literary resources data in the given XML file. 
# For PW, it is 'ls'.
def scrapeabbrv(abbrvtag):
	global entries # Fetched parse XML.
	g = codecs.open('abbrvwork/abbrvlist.txt', 'w','utf-8') # Opened file to store
	pw = entries.xpath('/pw/H1/body/'+abbrvtag) # Scraped only elements in XML tree which have the abbrvtag.
	wholeabbrvlist = [member.text for member in pw] # Created a list of the text of those elements.
	for member in wholeabbrvlist:
		if member is None:
			member = "" # A patch to overcome errors in windows for Nonetype.
		g.write(member.strip()+"\n") # Store one in a line in the storage file.
	g.close()
	return wholeabbrvlist # Also return a list.
print "Started scraping the abbreviations from pw.xml at ", printtimestamp()
print
# Change the abbrvtag with suitable tag if you want to extend the code for other dictionaries.
wholeabbrvlist = scrapeabbrv("ls")
print "Stored abbreviations in abbrvwork/abbrvilst.txt at ", printtimestamp()
print

def segregatepurenumbers():
	global wholeabbrvlist # Fetched global.
	n = codecs.open('abbrvwork/purenumberabbrvlist.txt','w','utf-8') # n for numbers
	a = codecs.open('abbrvwork/properrefs.txt','w','utf-8') # a for abbreviations (which we are interested in).
	properrefs = []
	for member in wholeabbrvlist:
		if member is None:
			member = ""
		if re.match(r'^([^a-zA-Z]*)$',member): # Removing improper reference tags.
			n.write(member+"\n")
		elif re.match(r'^([0-9a-z()&.,]+)$',member): # Same
			n.write(member+"\n")
		else:
			a.write(member+"\n") # Store proper tags in properrefs.txt
			properrefs.append(member) # Append to the list
	a.close()
	return properrefs # Return list

print "Segretating references with only numbers to abbrvwork/purenumberabbrvlist.txt and "
print "proper references to abbrvwork/properrefs.txt at", printtimestamp()
print
properrefs = segregatepurenumbers()
print "Completed segretating references at ", printtimestamp()
print

def removenumbers():
	global properrefs
	c = codecs.open('abbrvwork/cleanrefs.txt','w','utf-8')
	cleanrefs = []
	for member in properrefs:
		clean = re.sub(u'¨',u'$',member) # Some unicode issues sorted. Not converted them back as of now.
		clean = re.sub(u'›',u'$$',clean)
		clean = re.sub(u'ý',u'^2',clean)
		clean = re.sub(r'[.]([0-9,.a-z();\^\$]+)$','',clean) # Removed the trailing numbers of cantos / shlokas etc.
		clean = clean.strip('.') # Removed trailing period after the numbers are removed (if any).
		cleanrefs.append(clean)
	uniquerefs = list(set(cleanrefs)) # Return only the unique references.
	uniquerefs.sort() # Sort alphabetically.
	for mem1 in uniquerefs:
		c.write(mem1+"\n") # Write to cleanrefs.txt
	c.close()
	return (uniquerefs, cleanrefs) # Return a tuple with uniquerefs and cleanrefs as members. Both have their utility.
	
print "Removing numbers from properrefs and storing only names of works to abbrvwork/cleanrefs.txt at ", printtimestamp()
print
(uniquerefs, cleanrefs) = removenumbers()
print "Completed storing clean references at ", printtimestamp()
print

def occurrence():
	global cleanrefs, uniquerefs # Fetched from global
	abbstats = codecs.open('abbrvwork/stats.txt','w','utf-8') # sorting with statistics of occurrence.
	sortedcrefs = codecs.open('abbrvwork/sortedcrefs.txt','w','utf-8') # Only sorting. No statistics.
	occurlist = []
	for member in uniquerefs:
		occurlist.append( (member,cleanrefs.count(member)) ) # Appending a tuple (entry,occurrence) to the list.
	occurlist.sort(key=lambda x: x[1]) # Sorting by the number of the occurrences of a reference.
	for (x,y) in occurlist:
		abbstats.write(x+"-"+str(y)+"\n") # Added the count
		sortedcrefs.write(x+"\n") # No count
	sortedcrefs.close()
	abbstats.close()

print "Sorting the cleanrefs based on occurrences in pw.xml, and storing in sortedcrefs.txt"
print
print "Analysis of bibliographic references based on occurrences in pw.xml, and stored in stats.txt"
print
occurrence()
print "Execution ended at", printtimestamp()
print 
print "Total ", len(uniquerefs), "unique references"
print 
