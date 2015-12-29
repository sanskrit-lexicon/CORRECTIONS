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
	#print "Using xmlfile",xmlfilename
	# Function to return timestamp
	#print "Parsing started at", printtimestamp()
	entries = etree.parse(xmlfilename) # Parse xml
	#print "Parsing ended at", printtimestamp()
	return entries
def removecrap(word,dict):
	endrepl = [' puM',' strI',' klI',' tri',' [(].*[)]'] # for SKD and last one for YAT
	for a in endrepl:
		word = re.sub(a+'$','',word)
	if dict in ['acc','ap90']:
		word = re.sub('[=].*$','',word) # to overcome ACC entries like 'Izattantra = kAtantra'
	if dict == 'ap90':
		word = re.sub('-.*$','',word) # to overcome AP90 entries like 'aBinaMdanIya --naMdya'
	if dict in ['cae','ccs']:
		word = re.sub('[(](.*)[)]','\g<1>',word) # to ovecome CAE entries like '(kAma/)'
		word = word.replace('/','')
	if dict == 'gst':
		word = re.sub('[I]*[.][ ]','',word) # to overcome GST entries like 'I. ana'
	if dict in ['mci','yat','pd']:
		word = re.sub(' .*$','',word) # to overcome YAT entries like 'hoqa hoqati' or 'heza (f u) hezate'
		word = re.sub('[(].*[)]$','',word) # to overcome YAT entries like 'nAga.banDu(nDuH)'
	if dict == 'pgn':
		word = re.sub('\^[0-9]*$','',word) # to overcome PGN entries like 'candrApura^233'
	if dict == 'skd':
		word = re.sub(' .*$','',word) # to overcome SKD entries like 'atipanTAH [n] puM'
	if dict in ['wil']:
		word = re.sub('[(].*[)].*$','',word) # to overcome WIL entries like 'vapa(qu)quvapa'
	if dict in ['ap90']:
		word = re.sub('[(].*[)]$','',word)
	if not dict in ['pwg','pw']:
		word = re.sub('[(].*[)]','',word) # to overcome AP entries like 'Kawa(qa)kkikA'
	word = re.sub(',.*$','',word) # to overcome ACC entries like 'muktAvalIkiraRa, muktAvalIdIpikA, muktAvalIprakASa'	
	word = re.sub('^[0-9]','',word) # To handle BOP entries like '1. antara'
	word = re.sub('[^a-zA-Z0-9|~]','',word)
	word = re.sub('[0-9]$','',word)
	word = word.replace('*','')
	word = word.replace('^','') # to overcome PW entries like '(aryamya^)'
	return word

def scrape(dict):
	global counter
	entries = parsefile(dict) # Fetched parse XML.
	mwk1 = entries.xpath('/'+dict+'/*/h/key1')
	mwk2 = entries.xpath('/'+dict+'/*/h/key2')
	k1 = [etree.tostring(member, method="text", encoding='unicode') for member in mwk1]
	k2raw = [etree.tostring(member, encoding='unicode') for member in mwk2]
	k2 = [etree.tostring(member, method="text", encoding='unicode') for member in mwk2]
	print len(k1), 'entries to be examined.'
	#print 'Putting the mismatched entries in k1k2clash.txt.'
	for i in xrange(len(k2)):
		if dict == 'pd' and removecrap(k1[i],dict).strip() == removecrap(k2[i],dict).strip():
			pass
		elif not (k1[i].strip() == removecrap(k2[i],dict).strip()):
			g.write(dict+':'+k1[i]+':'+k2raw[i]+':'+k1[i]+':'+k2raw[i]+':n:\n')
			counter += 1

if __name__=="__main__":
	g = codecs.open('k1k2clash.txt', 'w','utf-8') # Opened file to store
	print "AE, AP90, BHS, BOR, KRM, MWE, PE, PUI, SCH, SHS, STC, VEI are not examined because of high false positives"
	dicts = ["ACC","AP90","AP","BEN","BOP","BUR","CAE","CCS","GRA","GST","IEG","INM","MCI","MD","MW72","MW","PD","PGN","PWG","PW","SKD","SNP","VCP","WIL","YAT"]
	counter = 0
	for dict in dicts:
		print "Treating dictionary", dict
		dict = dict.lower()
		scrape(dict)
		print
	print "Total", counter, "entries written to k1k2clash.txt"
	g.close()
