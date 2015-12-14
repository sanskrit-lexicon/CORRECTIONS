# -*- coding: utf-8 -*-
"""
ngram.py
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
def trypartition(word):
	global hw
	output = []
	for i in xrange(len(word)):
		if word[:i] in hw and word[i:] in hw:
			return True
			break
	else:
		return False

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
	dictin = sys.argv[1]
	nth = sys.argv[2]
	nth = int(nth)
	[basewords,testwords] = getbasewords(dictin)
	print "Fetching words which are previously tested and found OK"
	nochange = codecs.open('../nochange/nochange.txt','r','utf-8')
	noc = nochange.readlines()
	noc = triming(noc)
	alreadyprinted = codecs.open('output/printed.txt','r','utf-8')
	alreadypr = alreadyprinted.readlines()
	alreadyput = []
	for line in alreadypr:
		alreadyput.append(line.split(':')[2])
	print len(alreadyput)
	print "Creating base ngrams"
	basengrams = getngrams(basewords,nth)
	basengrams = set(basengrams)
	print "Created base ngrams"
	print "Started", nth, "gram generation."
	outfile = 'output/allvs'+dictin+'_'+str(nth)+'.txt'
	fout = codecs.open(outfile,'w','utf-8')
	print "Putting the output in", outfile
	for (word,dicts,lnums) in testwords:
		testwordengrams = set(getngrams([word],nth))
		if not testwordengrams <= basengrams and len(dicts)==1 and word not in noc and 'PD' not in dicts and not trypartition(word) and word not in alreadyput:
			differencelist = ','.join(list(testwordengrams - basengrams))
			if word not in noc and not re.search('r[kKgGcCjJwWqQtTdDpPbBmyrlvSzsh][kKgGcCjJwWqQtTdDpPbBmyrlvSzsh]',word) and not re.search('[HmM]$',word) and not re.search('[NYRnmM][kKgGcCjJwWqQtTdDpPbByrlvSzsh]',differencelist) and not re.search('[NYRnmM]$',differencelist) and not re.search('[NYRnmM][,]',differencelist):
				print word, dicts[0], list(testwordengrams - basengrams)
				fout.write(dicts[0].lower()+":"+word+','+lnums[0]+":"+word+":n:"+','.join(list(testwordengrams - basengrams))+"\n")
	fout.close()
	alreadyprinted.close()
