#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
import re
import codecs

def separate(filein,nochangefile,changefile):
	fin = codecs.open(filein,'r','utf-8')
	noch = codecs.open(nochangefile,'w','utf-8')
	ch = codecs.open(changefile,'w','utf-8')
	for line in fin:
		line = line.strip()
		if line[0] == ";":
			noch.write(line[1:]+"\n")
		else:
			ch.write(line+"\n")
	fin.close()
	noch.close()
	ch.close()

separate('abbrvoutput/finalabbrv.txt','abbrvoutput/nochange.txt','abbrvoutput/change.txt')
