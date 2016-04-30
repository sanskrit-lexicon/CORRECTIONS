# -*- coding: utf-8 -*-
import sys, re
import codecs
import string
import datetime
"""
Usage - python alphamismatch.py
Input - sanhw2.txt
This would find out words which are not in proper alphabetic order.
"""

# Function to return timestamp
def timestamp():
	return datetime.datetime.now()

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
def mwspecial():
	fin = codecs.open('../../../funderburkjim/MWderivations/step3/all.txt')
	data = fin.readlines()
	wordlnum = []
	for datum in data:
		datum = datum.strip()
		[h,l,k1,k2,type] = datum.split('\t')
		if h == "1":
			wordlnum.append((k1,l))
	return wordlnum
if __name__=="__main__":
	#print "Creating headword data of sanhw2.txt"
	sanhw2 = sanhw2('../../sanhw2/sanhw2.txt')
	#print "Created headword data of sanhw2.txt"
	dictionaryname = ["ACC","CAE","AE","AP90","AP","BEN","BHS","BOP","BOR","BUR","CCS","GRA","GST","IEG","INM","KRM","MCI","MD","MW72","MW","MWE","PD","PE","PGN","PUI","PWG","PW","SCH","SHS","SKD","SNP","STC","VCP","VEI","WIL","YAT"]
	for dictionary in dictionaryname:
		searchdict = dictionary
		#print 'Handling', searchdict
		counter = 0
		if searchdict == "MW":
			wordlnum = mwspecial()
		else:
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
		prevlnum = '0'
		prevword = ''
		alreadyprinted = 0
		"""
		The addendum in some dictionaries give false positives. The L-num of first headword of addenda are noted below, and ignored in the later code.
		ACC:Part 2 at 31312, Part 3 at 41686
		CCS:29706
		MCI:Part 1.2 starts at 440, Part 1.3 at 629, Part 1.4 at 837, Part 1.5 at 969, Part 1.6 at 2078, Part 1.7 at 2624
		MD:20700
		MW72:54542
		PWG:Firt addendum at 62407, Second addendum at 117929
		SCH:27661
		YAT:44416
		"""
		for (word,lnum) in data:
			if searchdict == 'MW' and (re.search(r'[.][0-9]$',lnum) or re.search(r'[.][0-9]$',prevlnum)):
				pass
			elif searchdict == 'ACC' and ((float(lnum) < 31312 and float(prevlnum) >= 31312) or (float(lnum) >= 31312 and float(prevlnum) < 31312) or (float(lnum) >= 41686 and float(prevlnum) < 41686) or (float(lnum) < 41686 and float(prevlnum) >= 41686)):
				pass
			elif searchdict == 'CCS' and ((float(lnum) < 29706 and float(prevlnum) >= 29706) or (float(lnum) >= 29706 and float(prevlnum) < 29706)):
				pass
			elif searchdict == 'MD' and ((float(lnum) < 20700 and float(prevlnum) >= 20700) or (float(lnum) >= 20700 and float(prevlnum) < 20700)):
				pass
			elif searchdict == 'MW72' and ((float(lnum) < 54542 and float(prevlnum) >= 54542) or (float(lnum) >= 54542 and float(prevlnum) < 54542)):
				pass
			elif searchdict == 'PWG' and ((float(lnum) < 62407 and float(prevlnum) >= 62407) or (float(lnum) >= 62407 and float(prevlnum) < 62407) or (float(lnum) >= 117929 and float(prevlnum) < 117929) or (float(lnum) < 117929 and float(prevlnum) >= 117929)):
				pass
			elif searchdict == 'SCH' and ((float(lnum) < 27661 and float(prevlnum) >= 27661) or (float(lnum) >= 27661 and float(prevlnum) < 27661)):
				pass
			elif searchdict == 'YAT' and ((float(lnum) < 44416 and float(prevlnum) >= 44416) or (float(lnum) >= 44416 and float(prevlnum) < 44416)):
				pass
			elif searchdict == 'MCI' and (float(lnum)-float(prevlnum) > 100 or float(prevlnum)-float(lnum) > 100):
				pass
			elif lnum < prevlnum:
				fout1.write(searchdict.lower()+':'+prevword+','+prevlnum+':'+prevword+':n:\n')
				fout1.write(searchdict.lower()+':'+word+','+lnum+':'+word+':n:\n')
				counter1 += 1
			if float(lnum) - float(prevlnum) > 1000 and not alreadyprinted == 1:
				#print searchdict, lnum
				alreadyprinted = 1
			prevlnum = lnum
			prevword = word
		print 'Found', counter1, 'mismatched words in', searchdict, 'dictionary'
		fout1.close()
	mwspecial()