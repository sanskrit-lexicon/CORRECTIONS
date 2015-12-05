# -*- coding: utf-8 -*-
"""
refactor.py
To weed out possible samAsas from file allvSMW_3.txt like files.
"""
import sys, re
import codecs
import string
import datetime
import split as s

# Function to return timestamp
def timestamp():
	return datetime.datetime.now()
def triming(lst):
	output = []
	for member in lst:
		member = member.strip()
		output.append(member)
	return output

if __name__ == "__main__":
	filename = sys.argv[1]
	fin = codecs.open(filename,'r','utf=8')
	data = fin.readlines()
	data = triming(data)
	fin.close()
	fout = codecs.open('refactored.txt','w','utf-8')
	for datum in data:
		[dict,wordwithlnum,word,errorcode,pattern] = datum.split(':')
		print word, s.trysplit(word)
		test = s.trypartition(word)
		if not test:
			fout.write(datum+"\n")
	fout.close()
