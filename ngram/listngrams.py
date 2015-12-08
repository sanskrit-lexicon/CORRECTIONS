# -*- coding: utf-8 -*-
"""
listngrams.py
To generate all possible ngrams in Sanskrit from sanhw2.txt

Input sanhw2.txt
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
	fin = codecs.open('../sanhw1/sanhw1.txt','r','utf-8')
	lines = fin.readlines()
	output = []
	for line in lines:
		line = line.strip() # 'aMSakalpanA:CAE,CCS,MD,MW,PD,PW'
		split = line.split(':') # ['aMSakalpanA', 'CAE,CCS,MD,MW,PD,PW']
		word = split[0] # 'aMSakalpanA'
		dicts = split[1].split(',') # ['CAE','CCS','MD','MW','PD','PW']
		output.append((split[0],dicts)) # ('aMSakalpanA', ['CAE','CCS','MD','MW','PD','PW'] )
	return output
def sanhw2():
	fin = codecs.open('../sanhw2/sanhw2.txt','r','utf-8')
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
sanhw2 = sanhw2()
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

def ngrams(input, n):
	output = []
	if n >= len(input): # Removing whole word entries.
		pass
	else:
		for i in range(len(input)-n+1):
			output.append(input[i:i+n])
	return output

def getngrams(words,nth):
	ngr = []
	for word in words:
		ngr += ngrams(word,nth)
	return ngr

if __name__=="__main__":
	lens = [len(word) for word in hw]
	maxlen = max(lens)
	allngrams = []
	for nth in range(1,maxlen):
		allngrams += getngrams(hw,nth)
	allngrams = list(set(allngrams))
	allngrams = sorted(allngrams,key=len)
	allngramtxt = codecs.open('allngramtxt.txt','w','utf-8')
	for member in allngrams:
		allngramtxt.write(member+"\n")
	allngramtxt.close()
	