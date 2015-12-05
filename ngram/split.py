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

def sanhw2():
	fin = codecs.open('../sanhw2/sanhw2.txt','r','utf-8')
	lines = fin.readlines()
	output = []
	for line in lines:
		line = line.strip()
		split = line.split(':') # ['aMSakalpanA', 'CAE;4,CCS;4,MD;4,MW;21,PD;50,PW;9']
		word = split[0] # 'aMSakalpanA'
		dictswithlnum = split[1].split(',') # ['CAE;4','CCS;4','MD;4','MW;21','PD;50','PW;9']
		for dictwlnum in dictswithlnum:
			dicts = []
			lnums = []
			[dict,lnum] = dictwlnum.split(';')
			dicts.append(dict) # ['CAE','CCS','MD','MW','PD','PW']
			lnums.append(lnum) # [4,4,4,21,50,9]
		output.append((word,dicts,lnums))
	return output
print "Creating headword data of sanhw2.txt"
sanhw2 = sanhw2()
hw = []
"""
for (word,dicts,lnums) in sanhw2:
	if 'MW' in dicts:
		hw.append(word)
"""
hw = [word for (word,dicts,lnums) in sanhw2]
print len(hw)
#hw = [word for (word,dicts,lnums) in sanhw2]	# Removed PD because of its too meticulous rare forms.
print "Created headword data of sanhw2.txt"

replas = [('kk','k'),('kK','K'),('gg','g'),('gG','G'),('NN','N'),('cc','c'),('cC','C'),('jj','j'),('jJ','J'),('YY','Y'),('ww','w'),('wW','W'),('qq','q'),('qQ','Q'),('RR','R'),('tt','t'),('tT','T'),('dd','d'),('dD','D'),('nn','n'),('pp','p'),('pP','P'),('bb','b'),('bB','B'),('mm','m'),('yy','y'),('rr','r'),('ll','l'),('vv','v'),('SS','S'),('zz','z'),('ss','s'),('hh','h'),('y','i'),('y','I'),('v','u'),('v','U'),]
def deduplicate(word):
	global replas
	for (a,b) in replas:
		word = word.replace(a,b)
	return word

term = [('A','a'),('I','i'),('AH','a'),('AH','as'),('aH','as'),('H',''),('m',''),('M',''),('O',''),('I','a'),('e','a')]
def determ(word):
	global term
	output = []
	if re.search('[AHImMO]$',word):
		for (a,b) in term:
			if re.search(a+'$',word):
				output.append(re.sub(a+'$',b,word))
	return output

def allngrams(input):
	output = []
	for n in range(2,len(input)):
		for i in range(len(input)-n+1):
			output.append(input[i:i+n])
	return output
def matchingngrams(ngrams):
	global hw
	return [ngram for ngram in ngrams if ngram in hw]
def trysplit(input):
	matchedngrams = matchingngrams(allngrams(input))
	startngrams = []
	for ngram in matchedngrams:
		if input.startswith(ngram):
			startngrams.append(ngram)
	startngrams = sorted(startngrams, key=len, reverse=True)
	for ngram in startngrams:
		remaining = input[len(ngram):]
		if (len(remaining) > 2 or remaining in ['tA']) and remaining in hw:
			return ngram+'+'+remaining
			break
		elif (len(remaining) > 2 or remaining in ['tA']):
			return ngram+'+'+trysplit(input[len(ngram):])
			break
	else:
		return input+'(WRONG)'

def trypartition(word):
	global hw
	dedup = deduplicate(word)
	deter = determ(word)
	deterdedup = determ(dedup)
	checklist = [word] + [dedup] + deter + deterdedup
	checklist = list(set(checklist))
	output = []
	for word in checklist:
		for i in xrange(len(word)):
			if word[:i] in hw and word[i:] in hw:
				return True
				break
			elif word[:i].endswith('eH') and word[:i-2]+'i' in hw and word[i:] in hw: # aditeHputra
				return True
				break
			elif word[:i] in hw and (word[i:-1]+'A' in hw or word[i:-1]+'I' in hw):	#anuzwubgarBA
				return True
				break
			elif not re.search('WRONG[)]$',trysplit(word)):
				return True
				break				
	else:
		return False

if __name__=="__main__":
	print timestamp()
	print trysplit(sys.argv[1])
	print timestamp()
