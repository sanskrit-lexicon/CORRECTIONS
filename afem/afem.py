# -*- coding: utf-8 -*-
""" afem.py

To generate words ending with 'a' and having feminine gender.
  
"""
import sys, re
import codecs
import string
import datetime

# Function to return timestamp
def timestamp():
	return datetime.datetime.now()

def afem(dict):
	fin = codecs.open("afem/"+dict+"_afem.xml","r","utf-8")
	fout = codecs.open("afem.txt","a","utf-8")
	data = fin.readlines()
	print "Extracting %s dictionary" % dict
	for line in data:
		if line.startswith('<H'):
			m = re.search('<key1>([a-zA-Z]*)</key1>',line)
			outdata = m.group(1)+":"+dict
			fout.write(outdata+"\n")

#dicts = ["ACC","CAE","AP90","AP","BEN","BHS","BOP","BUR","CCS","GRA","GST","IEG","INM","KRM","MCI","MD","MW72","MW","PD","PE","PGN","PUI","PWG","PW","SCH","SHS","SKD","SNP","STC","VCP","VEI","WIL","YAT"]
# Nothing in ACC, GST, IEG, INM, KRM, MCI, MD, PE, PGN, PUI, SHS, SNP, VEI, WIL,
# BHS grabbed manually.
dicts = ["AP90","AP","BEN","BOP","BUR","CAE","CCS","GRA","MW72","MW","PD","PW","PWG","SCH","SKD","VCP","YAT"]
for dict in dicts:
	afem(dict)
			