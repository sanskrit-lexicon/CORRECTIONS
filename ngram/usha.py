# -*- coding: utf-8 -*-
""" 
Usage -

python usha.py inputfile outputfile

e.g.

python link.py output/allvsMW_1.txt output/usha/allvsMW_1.txt
"""

import sys, re
import codecs
import string
import datetime
import transcoder

# Function to return timestamp
def timestamp():
	return datetime.datetime.now()

def triming(lst):
	output = []
	for member in lst:
		member = member.strip()
		output.append(member)
	return output

def linking(fin,fout):
	infile = codecs.open(fin,'r','utf-8')
	input = infile.readlines()
	input = triming(input)
	outfile = codecs.open(fout,'w','utf-8')
	#acc:akzoByatantre,41695:akzoByatantre:n:oBy -> acc:अक्षोभ्यतन्त्रे,41695:अक्षोभ्यतन्त्रे:n:oBy
	for line in input:
		[dict,headword,replica,errcode,note] = line.split(':')
		[hw,lnum] = headword.split(',')
		hw = transcoder.transcoder_processString(hw,'slp1','deva')
		note = transcoder.transcoder_processString(note,'slp1','deva')
		outfile.write(dict+':'+hw+','+lnum+':'+hw+':'+errcode+':'+note+'\n')
	outfile.close()
	print "Check", fout, "for testing"

if __name__=="__main__":
	fin = sys.argv[1]
	fout = sys.argv[2]
	linking(fin,fout)
	