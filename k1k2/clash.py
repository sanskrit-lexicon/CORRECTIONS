#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
from lxml import etree # lxml.de
import re
import codecs
import datetime
import sys

"""
Expected output -
dict:k1text:k2:k1text:k2:n
"""
def printtimestamp():
	return datetime.datetime.now()
#xmlfilename = sys.argv[1]  # e.g., ../pw.xml
def parsefile(dict):
	xmlfilename = '../../Cologne_localcopy/'+dict+'/'+dict+'xml/xml/'+dict+'.xml'
	print "Using xmlfile",xmlfilename
	# Function to return timestamp
	print "Parsing started at", printtimestamp()
	entries = etree.parse(xmlfilename) # Parse xml
	print "Parsing ended at", printtimestamp()
	return entries
def removecrap(word):
	endrepl = [' puM',' strI',' klI',' tri',' [(].*[)]'] # for SKD and last one for YAT
	for a in endrepl:
		word = re.sub(a+'$','',word)
	word = re.sub('^[0-9]','',word) # To handle BOP entries like '1. antara'
	word = re.sub('[^a-zA-Z0-9|~]','',word)
	word = re.sub('[0-9]$','',word)
	return word

def scrape(dict):
	entries = parsefile(dict) # Fetched parse XML.
	mwk1 = entries.xpath('/'+dict+'/*/h/key1')
	mwk2 = entries.xpath('/'+dict+'/*/h/key2')
	k1 = [etree.tostring(member, method="text", encoding='unicode') for member in mwk1]
	k2raw = [etree.tostring(member, encoding='unicode') for member in mwk2]
	k2 = [etree.tostring(member, method="text", encoding='unicode') for member in mwk2]
	print len(k1), 'entries to be examined.'
	print 'Putting the mismatched entries in k1k2clash.txt.'
	for i in xrange(len(k2)):
		if not (k1[i].strip() == removecrap(k2[i]).strip()):
			g.write(dict+':'+k1[i]+':'+k2raw[i]+':'+k1[i]+':'+k2raw[i]+':n:\n')

if __name__=="__main__":
	g = codecs.open('k1k2clash.txt', 'w','utf-8') # Opened file to store
	print "AE, AP90, BHS, BOR, KRM, MWE, PE, PUI, SCH, SHS, STC, VEI are not examined because of high false positives"
	dicts = ["ACC","AP","BEN","BOP","BUR","CAE","CCS","GRA","GST","IEG","INM","MCI","MD","MW72","MW","PD","PGN","PWG","PW","SKD","SNP","VCP","WIL","YAT"]
	for dict in dicts:
		print "Treating dictionary", dict
		dict = dict.lower()
		scrape(dict)
		print
	g.close()
