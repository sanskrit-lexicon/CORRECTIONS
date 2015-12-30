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
def astoslp(word):
	asslp = [('a1','A'),('i1','I'),('u1','U'),('r21','F'),('r2','f'),('ai','E'),('au','O'),('m2','M'),('h2','H'),('kh','K'),('gh','G'),('n3','N'),('ch','C'),('jh','J'),('n5','Y'),('t2h','W'),('t2','w'),('d2h','Q'),('d2','q'),('n2','R'),('th','T'),('dh','D'),('ph','P'),('bh','B'),('s4','S'),('s2','z'),]
	for (a,b) in asslp:
		word = word.replace(a,b)
	word = re.sub('([aAiIuUfFxXeEoO])[4]','\g<1>',word)
	return word
def stctoslp(word):
	word = re.sub(' \(.*$','',word)
	word1 = re.search(u'([-][ÇçA-Z0-9]+[-])$',word)
	word2 = re.search(u'(^[A-Z0-9]+[-])$',word)
	if word2:
		word = re.sub(u'(^[A-Z0-9]+[-])$',word2.group(1).lower(),word)
	if word1:
		word = re.sub(u'([-][ÇçA-Z0-9]+[-])$',word1.group(1).lower(),word)
	prep = [(u'Ç','S'),(u'ç','S'),]
	for (a,b) in prep:
		word = word.replace(a,b)
	word = astoslp(word)
	return word
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
	if dict in ['bhs','pui','sch','vei']:
		word = re.sub('^[?][ ]','',word) # to overcome BHS entries like '? Su1tkhalin'
		word = word[0].lower() + word[1:]
		word = astoslp(word)
		word = word.split('=')[0] # to overcome BHS entries like 'adhya1lamba = °bana'
	if dict == 'vei':
		word = re.sub('[.,]$','',word) # to overcome VEI entries like 'An2i1cin MOna.'
		word1 = re.search(' ([AIUEOKGNCJTDPBMYRLVSH])',word)
		if word1:
			word = re.sub(' ([AIUEOKGNCJTDPBMYRLVSH])',word1.group(1).lower(),word) # to overcome VEI entries like 'An2i1cin MOna.'
		word = astoslp(word)
		word = word.split('=')[0] # to overcome BHS entries like 'adhya1lamba = °bana'
	
	if dict == 'gst':
		word = re.sub('[I]*[.][ ]','',word) # to overcome GST entries like 'I. ana'
	if dict in ['mci','yat','pd']:
		word = re.sub(' .*$','',word) # to overcome YAT entries like 'hoqa hoqati' or 'heza (f u) hezate'
		word = re.sub('[(].*[)]$','',word) # to overcome YAT entries like 'nAga.banDu(nDuH)'
	if dict == 'pe':
		word = word.lower()
		word = word.replace('m3','m2')
		word = astoslp(word)
	if dict == 'pgn':
		word = re.sub('\^[0-9]*$','',word) # to overcome PGN entries like 'candrApura^233'
	if dict == 'sch':
		word = re.sub('[()]','',word) # to overcome SCH entries like 'an3ka1y(ate)'
	if dict == 'shs':
		word = re.sub('[(].*$','',word) # to overcome SHS entries like 'kana(I Yi)YikanI'
	if dict == 'skd':
		word = re.sub(' .*$','',word) # to overcome SKD entries like 'atipanTAH [n] puM'
	if dict == 'stc':
		word = word.replace(u'ç','S') # to overcome STC entries like 'aMça-'
		word = stctoslp(word) # to overcome STC entries like 'ati-SAD-'
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
	print "AE, BOR, KRM and MWE are not examined because of high false positives"
	dicts = ["ACC","AP90","AP","BEN","BHS","BOP","BUR","CAE","CCS","GRA","GST","IEG","INM","MCI","MD","MW72","MW","PD","PGN","PWG","PW","SCH","SHS","SKD","SNP","STC","VCP","VEI","WIL","YAT"]
	print "PUI pending to be handled. Some odd encoding."
	counter = 0
	for dict in dicts:
		print "Treating dictionary", dict
		dict = dict.lower()
		scrape(dict)
	print "Total", counter, "entries written to k1k2clash.txt"
	g.close()
