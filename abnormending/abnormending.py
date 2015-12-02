# -*- coding: utf-8 -*-
""" abnormending.py

To generate words ending with abnormal endings (maybe less than 50 headwords).
  
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

def abnormending():
	fout = codecs.open('abnorm.txt','w','utf-8')
	fin = codecs.open("../sanhw1/sanhw1.txt","r","utf-8")
	data = fin.readlines()
	data = triming(data)
	output = []
	for datum in data:
		[word,dict] = datum.split(':')
		output.append((word[-2:],datum))
	endings = []
	for (end,datu) in output:
		if end not in endings:
			endings.append(end)
	print len(endings)
	withcounter = []
	for ends in endings:
		counter = 0
		for datum in data:
			if re.search(ends+':',datum):
				counter += 1
		if counter < 50:
			withcounter.append((counter, ends))
			print counter, ends
	withcounter = sorted(withcounter,key=lambda x: x[0])
	print "Culled out and sorted abnormal endings"
	
	print "Writing suspect entries to abnorm.txt."
	print "This would take some time."
	nochange = codecs.open('../nochange/nochange1.txt','r','utf-8')
	noc = nochange.readlines()
	noc = triming(noc)
	for (count,end) in withcounter:
		for datum in data:
			if re.search(end+':[^,]*$',datum) and datum not in noc:
				fout.write(datum+"\n")
	fout.close()
	
abnormending()
	
