# -*- coding: utf-8 -*-
"""
To generate 2-grams and 3-grams which are found in ALL of the following dictionaries.

Usage:
python commonngrams.py n
e.g.
python commonngrams.py 3
would create 3-grams which are found in all of the following dictionaries.

Dictionaries
MW PW PWG PD MW72 VCP SHS YAT WIL SKD CAE AP ACC AP90 CCS SCH STC MD BUR BHS BEN
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
print timestamp()
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
	ngr = list(set(ngr))
	return ngr
def commons(lstoflist,n):
	commons = []
	filestore = codecs.open('commonngram/'+str(n)+'grams.txt','w','utf-8')
	for member in lstoflist[-1]:
		if all(member in lst for lst in lstoflist):
			commons.append(member)
			filestore.write(member+"\n")
	print "Common ngrams are", len(commons)
	filestore.close()
	return commons
def commonngram(n):	
	#majordicts = ["MW","PW","PWG","PD","MW72","VCP","SHS","YAT","WIL","SKD","CAE","AP","ACC","AP90","CCS","SCH","STC","MD","BUR","BHS","BEN"]
	majordicts = ["MW","PW"]
	ngrams = []
	for dict in majordicts:
		print dict
		[basewords,otherwords] = getbasewords(dict)
		ngram = getngrams(basewords,n)
		print len(ngram)
		ngrams.append(ngram)
	commonngrams = commons(ngrams,n)	
def testwithcommonngrams(testfile,n):
	whitelist = set(['eH','AH','EH'])
	textfile = codecs.open(testfile,'r','utf-8')
	lines = textfile.readlines()
	lines = triming(lines)
	errorfile = codecs.open('commonngram/error.txt','w','utf-8')
	basefile = codecs.open('commonngram/'+str(n)+'grams.txt','r','utf-8')
	basengrams = basefile.read().split()
	basengrams = triming(basengrams)
	basefile.close()
	counter = 0
	for line in lines:
		line = line.replace('-',' ')
		testwords = line.split(' ')
		for testword in testwords:
			testword = re.sub('[\'",.?0-9!]','',testword)
			testngrams = ngrams(testword,n)
			diff = set(testngrams)-set(basengrams)
			if not diff < whitelist:
				diff = list(diff)
				if len(diff) is not 0:
					print testword, diff
					errorfile.write(testword+':'+','.join(diff)+'\n')
					counter += 1
	errorfile.close()
	print "Total potential errors by ngram method are", counter
	
if __name__=="__main__":
	n = sys.argv[1]
	#commonngram(int(n))
	testwithcommonngrams('commonngram/test.txt',int(n))
	