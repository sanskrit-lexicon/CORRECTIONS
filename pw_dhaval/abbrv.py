#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
from lxml import etree
import re
import codecs
import datetime

"""
# Abbreviations of PW
Run `python abbrv.py` from pywork directory to regenerate the lists.

# Dependencies
[lxml](http://lxml.de/) to parse pw.xml

# Logic
1. `<ls>something</ls>` tag usually holds the literary source data.

2. The text `something` is scraped via lxml and stored in abbrvlist.txt file (1st raw file).

3. abbrvlist.txt file still has some references which are pure numbers. We have discarded them as of now and stored them in purenumberabbrvlist.txt (byproduct). (See https://github.com/sanskrit-lexicon/PWK/issues/11 for details).

4. The list which is not pure numbers, but has some alphabet preceding it is stored in properrefs.txt (raw file 2).

5. The properrefs.txt file still has entries like `TA7N2D2JA-BR.25,13,3.` where the last entries are the canto / shloka number. They need to be removed.

6. The canto or shloka numbers are removed and only unique entries are kept in cleanrefs.txt (final product).
"""

# Function to return timestamp
def printtimestamp():
	return datetime.datetime.now()
print "Parsing started at", printtimestamp()
entries = etree.parse('pw.xml') # Parse xml
print "Parsing ended at", printtimestamp()

def scrapeabbrv():
	global entries # Fetched parse XML.
	g = codecs.open('abbrvwork/abbrvlist.txt', 'w','utf-8') 
	pw = entries.xpath('/pw/H1/body/ls')
	wholeabbrvlist = [member.text for member in pw]
	for member in wholeabbrvlist:
		if member is None:
			member = ""
		g.write(member.strip()+"\n")
	g.close()
	return wholeabbrvlist
print "Started scraping the abbreviations from pw.xml at ", printtimestamp()
wholeabbrvlist = scrapeabbrv()
print "Stored abbreviations in abbrvwork/abbrvilst.txt at ", printtimestamp()

def segregatepurenumbers():
	global wholeabbrvlist
	n = codecs.open('abbrvwork/purenumberabbrvlist.txt','w','utf-8')
	a = codecs.open('abbrvwork/properrefs.txt','w','utf-8')
	properrefs = []
	for member in wholeabbrvlist:
		if member is None:
			member = ""
		if re.match(r'^([^a-zA-Z]*)$',member):
			n.write(member+"\n")
		elif re.match(r'^([0-9a-z()&.,]+)$',member):
			n.write(member+"\n")
		else:
			a.write(member+"\n")
			properrefs.append(member)
	a.close()
	return properrefs

print "Segretating references with only numbers to abbrvwork/purenumberabbrvlist.txt and "
print "proper references to abbrvwork/properrefs.txt at", printtimestamp()
properrefs = segregatepurenumbers()
print "Completed segretating references at ", printtimestamp()

def removenumbers():
	global properrefs
	c = codecs.open('abbrvwork/cleanrefs.txt','w','utf-8')
	cleanrefs = []
	for member in properrefs:
		clean = re.sub(u'¨',u'$',member)
		clean = re.sub(u'›',u'$$',clean)
		clean = re.sub(u'ý',u'^2',clean)
		clean = re.sub(r'[.]([0-9,.a-z();\^\$]+)$','',clean)
		cleanrefs.append(clean)
	uniquerefs = list(set(cleanrefs))
	uniquerefs.sort()
	for mem1 in uniquerefs:
		c.write(mem1+"\n")
	c.close()
	return (uniquerefs, cleanrefs)
	
print "Removing numbers from properrefs and storing only names of works to abbrvwork/cleanrefs.txt at ", printtimestamp()
(uniquerefs, cleanrefs) = removenumbers()
print "Completed storing clean references at ", printtimestamp()

def occurrence():
	global cleanrefs, uniquerefs
	abbstats = codecs.open('abbrvwork/stats.txt','w','utf-8')
	sortedcrefs = codecs.open('abbrvwork/sortedcrefs.txt','w','utf-8')
	occurlist = []
	for member in uniquerefs:
		print member
		occurlist.append( (member,cleanrefs.count(member)) )
	occurlist.sort(key=lambda x: x[1])
	for (x,y) in occurlist:
		abbstats.write(x+"-"+str(y)+"\n")
		sortedcrefs.write(x+"\n")
	sortedcrefs.close()
	abbstats.close()
occurrence()