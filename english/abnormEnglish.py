# -*- coding: utf-8 -*-
"""
Author:
	Dr. Dhaval Patel, 15 November 2017
Author:
	Dr. Dhaval Patel, 06 October 2016
Expected output:
	To find out abnormal headwords from dictionaries having English headwords like AE.
Input:
	../../Cologne_localcopy/ae/orig/ae.txt
Output:
	output/ae_abnorm.txt
Usage:
	python abnormEnglish.py dictname
	e.g.
	python abnormEnglish.py AE
"""

import sys, re
import codecs
import enchant
from ngram import NGram
import nltk.corpus
import pickle

def reHeadword(dictname):
	if dictname == 'ae':
		return '^<P>{@([A-Za-z]+)[,.]@}'
	
if __name__=="__main__":
	dictname = sys.argv[1]
	dictname = dictname.lower()
	"""
	print "Step 1. Store the words not found in pyenchant as dictname_abnorm.txt"
	fin = codecs.open('../../Cologne_localcopy/'+dictname+'/orig/'+dictname+'.txt','r','utf-8')
	reH = reHeadword(dictname)
	eng_dict = enchant.Dict('en_GB')
	fout = codecs.open(dictname+'_abnorm.txt','w','utf-8')
	for line in fin:
		matc = re.search(reH,line)
		if matc:
			headword = matc.group(1)
			if not eng_dict.check(headword):
				print headword
				fout.write(headword+'\n')
	fin.close()
	fout.close()
	"""
	
	# Generate trigrams from NLTK and ngram modules and store in pickle file for future use
	# If you want to regenerate, please change generateNgram to True
	generateNgram = False
	if generateNgram:
		entrigram = open('en_trigrams.pickle','w')
		en_word_list = nltk.corpus.abc.words()
		n = NGram()
		ngset = set()
		counter = 0
		for word in en_word_list:
			counter += 1
			word = word.lower()
			ngset = ngset.union(set(n._split(word)))
			if counter % 10000 == 0:
				print counter
				print len(ngset)
		pickle.dump(ngset,entrigram)

	print "Step 2. Store the words not found in pyenchant as dictname_abnorm.txt"
	fin2 = codecs.open(dictname+'_abnorm.txt','r','utf-8')
	entrigram = open('en_trigrams.pickle')
	ngset = pickle.load(entrigram)
	print len(ngset)
	for line in fin2:
		line = line.lower()
		line = line.rstrip()
		trig = set(NGram()._split(line))
		dif = trig.difference(ngset)
		if dif:
			print line, dif
