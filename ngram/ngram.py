# -*- coding: utf-8 -*-
""" ngram.py

To generate words having unique ngrams. 
  
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
	fin = codecs.open('../sanhw1/sanhw1.txt','r','utf-8');
	lines = fin.readlines()
	output = []
	for line in lines:
		line = line.strip() # 'aMSakalpanA:CAE,CCS,MD,MW,PD,PW'
		split = line.split(':') # ['aMSakalpanA', 'CAE,CCS,MD,MW,PD,PW']
		word = split[0] # 'aMSakalpanA'
		dicts = split[1].split(',') # ['CAE','CCS','MD','MW','PD','PW']
		output.append((split[0],dicts)) # ('aMSakalpanA', ['CAE','CCS','MD','MW','PD','PW'] )
	return output

def getbasewords(basedict):
	headwithdicts = sanhw1()
	basewords = []
	otherwords = []
	for (word,dicts) in headwithdicts:
		if basedict in dicts:
			basewords.append(word)
		else:
			otherwords.append((word,dicts))
	return [basewords,otherwords]

def ngrams(input, n):
  output = []
  for i in range(len(input)-n+1):
    output.append(input[i:i+n])
  return output
  
def getengrams(words,nth):
	ngr = []
	for word in words:
		for i in range(1,nth):
			ngr += ngrams(word,i)
	return ngr

		
if __name__=="__main__":
	dictin = sys.argv[1]
	nth = sys.argv[2]
	nth = int(nth)
	outfile = 'allvs'+dictin+'_'+str(nth)+'.txt'
	fout = codecs.open(outfile,'w','utf-8')
	[basewords,testwords] = getbasewords(dictin)
	print "Creating base ngrams"
	basengrams = getengrams(basewords,nth)
	basengrams = set(basengrams)
	print "Created base ngrams"
	for (word,dicts) in testwords:
		testwordengrams = set(getengrams([word],nth))
		if not testwordengrams <= basengrams and len(dicts)==1:
			if not re.search('r[kKgGcCjJwWqQtTdDpPbBmyrlvSzsh][kKgGcCjJwWqQtTdDpPbBmyrlvSzsh]',word) and not re.search('[HmM]$',word):
				print word, list(testwordengrams - basengrams)
				fout.write(word+":"+','.join(dicts)+":"+','.join(list(testwordengrams - basengrams))+"\n")
	fout.close()
