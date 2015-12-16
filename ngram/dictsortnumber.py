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

dictionaries = ["ACC","CAE","AP90","AP","BEN","BHS","BOP","BUR","CCS","GRA","GST","IEG","INM","KRM","MCI","MD","MW72","MW","PD","PE","PGN","PUI","PWG","PW","SCH","SHS","SKD","SNP","STC","VCP","VEI","WIL","YAT"]
dictcount = []
for dict in dictionaries:
	counter = 0
	for (word,dicts,lnums) in sanhw2:
		if dict in dicts:
			counter += 1
	dictcount.append((dict,counter))
dictcount = sorted(dictcount, key=lambda x:x[1], reverse=True)
#print dictcount
# [('MW', 193893), ('PW', 131919), ('PWG', 106079), ('PD', 104934), ('MW72', 51152), ('VCP', 47095), ('SHS', 46705), ('YAT', 44720), ('WIL', 43939), ('SKD', 40519), ('CAE', 38438), ('AP', 36028), ('ACC', 32128), ('AP90', 31160), ('CCS', 28762), ('SCH', 28448), ('STC', 23989), ('MD', 20102), ('BUR', 19129), ('BHS', 17733), ('BEN', 17017), ('PUI', 12148), ('GRA', 10243), ('INM', 9463), ('BOP', 8499),('IEG', 7555), ('GST', 6761), ('PE', 6634), ('VEI', 3705), ('MCI', 2319), ('KRM', 1689), ('PGN', 470), ('SNP', 448)]
dictsorted = [a for (a,b) in dictcount]	
print '["'+'","'.join(dictsorted)+'"]'
#["MW","PW","PWG","PD","MW72","VCP","SHS","YAT","WIL","SKD","CAE","AP","ACC","AP90","CCS","SCH","STC","MD","BUR","BHS","BEN","PUI","GRA","INM","BOP","IEG","GST","PE","VEI","MCI","KRM","PGN","SNP"]
# Only ["MW","PW","PWG","PD","MW72","VCP","SHS","YAT","WIL","SKD","CAE","AP","ACC","AP90","CCS","SCH","STC","MD","BUR","BHS","BEN"] is used. Rest give a lot of false positives.
