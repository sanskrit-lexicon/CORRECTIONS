# -*- coding: utf-8 -*-
import sys, re
import codecs
import string
import datetime
import itertools

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
	fin = codecs.open('../CORRECTIONS/sanhw2/sanhw2.txt','r','utf-8')
	lines = fin.readlines()
	output = []
	for line in lines:
		line = line.strip()
		split = line.split(':') # ['aMSakalpanA', 'CAE;4,CCS;4,MD;4,MW;21,PD;50,PW;9']
		word = split[0] # 'aMSakalpanA'
		dictswithlnum = split[1].split(',') # ['CAE;4','CCS;4','MD;4','MW;21','PD;50','PW;9']
		print dictswithlnum
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
hw = []
for (word,dicts,lnums) in sanhw2:
	if 'MW' in dicts:
		hw.append(word)
#hw = [word for (word,dicts,lnums) in sanhw2]
print len(hw)
print "Created headword data of sanhw2.txt"
def unique(lst):
	output = []
	for member in lst:
		if member not in output:
			output.append(member)
	return output

# Asked the procedure at http://stackoverflow.com/questions/34108900/optionally-replacing-a-substring-python
lstrep = [('A',('A','aa','aA','Aa','AA')),('I',('I','ii','iI','Ii','II')),('U',('U','uu','uU','Uu','UU')),('F',('F','ff','fx','xf','Fx','xF','FF')),('e',('e','ea','ai','aI','Ai','AI')),('o',('o','oa','au','aU','Au','AU','aH','aHa')),('E',('E','ae','Ae','aE','AE')),('O',('O','ao','Ao','aO','AO'))]	
global solutions
solutions = {}
def permut(word,lstrep,dictionary):
	input_str = word

	# make substitution list a dict for easy lookup
	lstrep_map = dict(lstrep)
	# a substitution is an index plus a string to substitute. build
	# list of subs [[(index1, sub1), (index1, sub2)], ...] for all
	# characters in lstrep_map.
	subs = []
	for i, c in enumerate(input_str):
		if c in lstrep_map:
			subs.append([(i, sub) for sub in lstrep_map[c]])
	# build output by applying each sub recorded
	out = []
	for sub in itertools.product(*subs):
		# make input a list for easy substitution
		input_list = list(input_str)
		for i, cc in sub:
			if ''.join(input_list[:i])+cc[0] in dictionary:
				input_list[i] = cc
			input_list[i] = cc
		out.append(''.join(input_list))
	out = unique(out)
	out = sorted(out, key=len)
	return out

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
	perm = permut(sys.argv[1],lstrep,hw)
	print timestamp()
	for word in perm:
		print trysplit(word)
	print timestamp()
	
