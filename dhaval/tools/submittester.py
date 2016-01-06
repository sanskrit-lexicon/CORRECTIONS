# -*- coding: utf-8 -*-
import sys, re
import codecs
import datetime

"""
Dr. Dhaval Patel
3 Jan 2016
Code to make sure that the submission in standard format is proper.
Display fishy entries on console.

Usage:
python submittester.py filepath submissiontype
where submissiontype is 1 for headword submissions and 2 for literary resources submissions

Input:
File in standard format
1. dictcode:oldword:newword:errorcode:notes   # Useful for headword correction submissions
e.g. ieg:awWAimahotsava,645:awWAimahotsava:n:Ai
or
2. oldword@key1@key2@lnum:newword:errorcode:notes   # Useful for bibliographic / other textual corrections.
e.g. ¯AGN.¯P.@SAlagrAma@SAlagrAma@111783:¯AGNI.P.:t:Not two separate references.

Logic:
Try to find out submissions where 
1. oldword == newword but standardconvention != 'n'
or
2. oldword != newword but standardconvention == 'n'

Currently code prints it on screen, as this is just a testing machine, so that no error gets passed.
Not storing the errors somewhere else as log file.
"""

# Function to return timestamp
def timestamp():
	return datetime.datetime.now()

def scrapedetails(file,submissiontype):
	fin = codecs.open(file,'r','utf-8')
	lines = fin.readlines()
	errorlist = []
	for line in lines:
		line = line.strip()
		parts = line.split(':')
		if submissiontype == '1':
			oldword = parts[1].split(',')[0]
			newword = parts[2]
			errorcode = parts[3]
		if submissiontype == '2':
			oldword = parts[0].split('@')[0]
			newword = parts[1]
			errorcode = parts[2]
		if oldword == newword and not errorcode == 'n':
			errorlist.append((oldword,newword,errorcode,line,1))
		elif errorcode == 'n' and not oldword == newword:
			errorlist.append((oldword,newword,errorcode,line,2))
	if len(errorlist) > 0:
		for (oldword,newword,errorcode,line,errortype) in errorlist:
			if errortype == 1:
				print 'equal words, but errorcode not "n"'
				print line.encode('utf-8')
				print '-'*30
			elif errortype == 2:
				print 'different words, but errorcode is "n"'
				print line.encode('utf-8')
				print '-'*30
	else:
		print 'All entries are OK'

if __name__=="__main__":
	filename = sys.argv[1]
	submissiontype = sys.argv[2]
	print
	print 'Examining', filename
	print
	scrapedetails(filename,submissiontype)
	print
