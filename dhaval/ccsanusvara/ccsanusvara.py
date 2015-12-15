# -*- coding: utf-8 -*-
"""
ccsanusvara.py

To generate list of words having anusvAra in CCS and the word without anusvara is in sanhw2.txt

See issue https://github.com/sanskrit-lexicon/CORRECTIONS/issues/201 for details.

Usage
python ccsanusvara.py
"""
import sys, re
import codecs
import string
import datetime

# Function to return timestamp
def timestamp():
	return datetime.datetime.now()

def triming(lst):
	output = []
	for member in lst:
		member = member.strip()
		output.append(member)
	return output

# Create a list of (word,dictionarylist) tuple.
def sanhw1():
	fin = codecs.open('../../sanhw1/sanhw1.txt','r','utf-8')
	lines = fin.readlines()
	output = []
	for line in lines:
		line = line.strip() # 'aMSakalpanA:CAE,CCS,MD,MW,PD,PW'
		split = line.split(':') # ['aMSakalpanA', 'CAE,CCS,MD,MW,PD,PW']
		word = split[0] # 'aMSakalpanA'
		dicts = split[1].split(',') # ['CAE','CCS','MD','MW','PD','PW']
		output.append((split[0],dicts)) # ('aMSakalpanA', ['CAE','CCS','MD','MW','PD','PW'] )
	return output
# Read data in sanhw2.txt format
def sanhw2(inputfile):
	fin = codecs.open(inputfile,'r','utf-8')
	lines = fin.readlines()
	output = []
	for line in lines:
		line = line.strip()
		split = line.split(':') # ['aMSakalpanA', 'CAE;4,CCS;4,MD;4,MW;21,PD;50,PW;9']
		word = split[0] # 'aMSakalpanA'
		dictswithlnum = split[1].split(',') # ['CAE;4','CCS;4','MD;4','MW;21','PD;50','PW;9']
		dicts = []
		lnums = []
		for dictwlnum in dictswithlnum:
			[dict,lnum] = dictwlnum.split(';')
			dicts.append(dict) # ['CAE','CCS','MD','MW','PD','PW']
			lnums.append(lnum) # [4,4,4,21,50,9]
		output.append((word,dicts,lnums))
	return output
print "Creating headword data of sanhw2.txt"
sanhw2 = sanhw2('../../sanhw2/sanhw2.txt')
hw = [word for (word,dicts,lnums) in sanhw2]	
print "Created headword data of sanhw2.txt"

fout = codecs.open('ccsanusvara.txt','w','utf-8')
for (word,dicts,lnums) in sanhw2:
	rep = word.replace('M','')
	if 'CCS' in dicts and len(dicts) == 1 and re.search('M',word) and word is not rep and rep in hw:
		print word, word.replace('M','')
		fout.write('ccs:'+word+':'+rep+':n:\n')
fout.close()
	