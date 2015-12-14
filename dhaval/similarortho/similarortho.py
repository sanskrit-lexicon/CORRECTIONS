# -*- coding: utf-8 -*-
""" similarortho.py

To generate list of words having similar orthography.
e.g. k-P, g-m-r, G-D, c-v, w-w-q-Q, dv-dD, n-m, p-y, M-blank, S-z-s

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
def getbasewords(basedict):
	global sanhw2
	headwithdicts = sanhw2
	basewords = []
	otherwords = []
	for (word,dicts,lnums) in headwithdicts:
		if basedict in dicts:
			basewords.append(word)
		else:
			otherwords.append((word,dicts,lnums))
	return [basewords,otherwords]

def dictlnumback(dicts,lnums):
	output = ''
	for i in xrange(len(dicts)):
		output += ","+dicts[i]+";"+lnums[i]
	output = output.strip(',')
	return output
def generatesimilars(headword):
	#k-P, g-m-r, G-D, c-v, w-W-q-Q, dv-dD, n-m, p-y, M-blank, S-z-s
	#lst1 = [('k',('P')),('P',('k')),('g',('m','r')),('m',('g','r')),('r',('m','g')),('G',('D')),('D',('G')),('w',('W','q','Q')),('W',('w','q','Q')),('q',('w','W','Q')),('Q',('w','W','q')),('dv',('dD')),('dD',('dv')),('n',('m')),('m',('n')),('M',('')),('S',('z','s')),('z',('S','s')),('s',('S','z')),]
	lst1 = [('G',('D')),('D',('G'))]
	output = []
	for (a,b) in lst1:
		for bb in b:
			output.append(headword.replace(a,bb))
	output = list(set(output))
	return output
def similarortho():
	global sanhw2, hw
	outfile = codecs.open('DGconf.txt','w','utf-8')
	for (headword,dicts,lnums) in sanhw2:
		for member in generatesimilars(headword):
			if member is not headword and member in hw :
				print headword, member
				outfile.write(headword+":"+member+"\n")
	outfile.close()
similarortho()				
			
	
