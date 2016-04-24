# -*- coding: utf-8 -*-
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

if __name__=="__main__":
	#print "Creating headword data of sanhw2.txt"
	sanhw2 = sanhw2('../../sanhw2/sanhw2.txt')
	#print "Created headword data of sanhw2.txt"
	dictionaryname = ["ACC","CAE","AE","AP90","AP","BEN","BHS","BOP","BOR","BUR","CCS","GRA","GST","IEG","INM","KRM","MCI","MD","MW72","MW","MWE","PD","PE","PGN","PUI","PWG","PW","SCH","SHS","SKD","SNP","STC","VCP","VEI","WIL","YAT"]
	for dictionary in dictionaryname:
		searchdict = dictionary
		#print 'Handling', searchdict
		#fout = codecs.open('withlnum/'+searchdict+'withlnum.txt','w','utf-8')
		counter = 0
		wordlnum = []
		for (word,dicts,lnums) in sanhw2:
			for x in xrange(len(dicts)):
				if dicts[x] == searchdict:
					counter += 1
					wordlnum.append((word,lnums[x]))
		#print 'Wrote', counter, 'words'
		fout1 = codecs.open('mismatch/'+searchdict+'mismatch.txt','w','utf-8')
		counter1 = 0
		data = wordlnum
		prevlnum = 0
		prevword = ''
		for (word,lnum) in data:
			if lnum < prevlnum:
				fout1.write(searchdict.lower()+':'+prevword+','+prevlnum+':'+prevword+':n:\n')
				fout1.write(searchdict.lower()+':'+word+','+lnum+':'+word+':n:\n')
				counter1 += 1
			prevlnum = lnum
			prevword = word
		print 'Found', counter1, 'mismatched words in', searchdict, 'dictionary'
		fout1.close()
