# -*- coding: utf-8 -*-
"""
ngram.py
To generate words having unique ngrams.   
"""
import sys, re
import codecs
import string
import datetime
from math import log
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

def ngrams(input, n):
	output = []
	if n >= len(input): # Removing whole word entries.
		pass
	else:		
		for i in range(len(input)-n+1):
			output.append(input[i:i+n])
	return output

def getngrams(words,nth):
	ngr = []
	for word in words:
		ngr += ngrams(word,nth)
	ngr = set(ngr)
	return ngr

def getwords(data,dict,lineinput=False):
	words = []
	
	if not lineinput:
		print len(data), 'lines to read and process'
		if dict in ['ap90','ap','ben','bhs','bor','pd','ae','mw72','stc']:
			entries = re.split(r'[<][P][>]',data)
		elif dict in ['vcp','skd','pw','pwg','bop','gst','mwe','shs','yat']:
			entries = re.split('[<]H[1I][>]',data)
		elif dict in ['wil']:
			parts = re.findall('[.]E[.]',line)
		elif dict in ['bur']:
			parts = re.findall('[.][{][#]',line)
		print len(entries), 'entries total'
		for line in entries:
			line = line.strip()
			line = line.lstrip('<HI>')
			# AS1 to SLP1 conversion for necessary dictioanries.
			if dict in ['ben']:
				line = line.lower()
				line = transcoder.transcoder_processString(line,'ben','slp1')
			elif dict in ['bur']:
				line = line.lower()
				line = transcoder.transcoder_processString(line,'bur','slp1')
			elif dict in ['mw72']:
				line = line.lower()
				line = transcoder.transcoder_processString(line,'mw72','slp1')
			elif dict in ['bhs','sch','stc']:
				line = line.lower()
				line = transcoder.transcoder_processString(line,'as','slp1')
			line = re.sub('\[.*\]','',line)
			line = re.sub('[0-9]','',line)
			line = line.replace('^','')
			line = line.replace("\\","")
			if dict in ['skd','vcp']:
				parts = [line]
			elif dict in ['ap','ap90','ae','bop','bor','gst','mwe','pd','shs','wil','yat']:
				parts = re.findall('\{#([^#]*)#\}',line)
			elif dict in ['pwg']:
				parts = re.findall('\{#([^}]*)[#]*\}',line)
			elif dict in ['pw']:
				parts = re.findall('#\{([^}]*)\}',line)
			elif dict in ['ben','bur','mw72','sch','stc']:
				parts = re.findall('\{%([^%]*)%}',line)
			elif dict in ['bhs']:
				parts = re.findall('\{@([^@]*)@}',line)
			for part in parts:
				words += re.split('\W+',part)
	else:
		line = data
		line = line.strip()
		line = line.lstrip('<HI>')
		# AS1 to SLP1 conversion for necessary dictioanries.
		if dict in ['ben']:
			line = line.lower()
			line = transcoder.transcoder_processString(line,'ben','slp1')
		elif dict in ['bur']:
			line = line.lower()
			line = transcoder.transcoder_processString(line,'bur','slp1')
		elif dict in ['mw72']:
			line = line.lower()
			line = transcoder.transcoder_processString(line,'mw72','slp1')
		elif dict in ['bhs','sch','stc']:
			line = line.lower()
			line = transcoder.transcoder_processString(line,'as','slp1')
		line = re.sub('\[.*\]','',line)
		line = re.sub('[0-9]','',line)
		line = line.replace('^','')
		line = line.replace('\\','')
		if dict in ['skd','vcp']:
			parts = [line]
		elif dict in ['ap','ap90','ae','bop','bor','gst','mwe','pd','shs','wil','yat']:
			parts = re.findall('\{#([^#]*)#\}',line)
		elif dict in ['pwg']:
			parts = re.findall('\{#([^}]*)[#]*\}',line)
		elif dict in ['pw']:
			parts = re.findall('#\{([^}]*)\}',line)
		elif dict in ['ben','bur','mw72','sch']:
			parts = re.findall('\{%([^%]*)%}',line)
		elif dict in ['bhs']:
			parts = re.findall('\{@([^@]*)@}',line)
		for part in parts:
			words += re.split('\W+',part)
		
	words = [member for member in words if len(member) > 1]
	words = set(words)
	return words

if __name__=="__main__":
	handleddictlist = ['ap90','ap','ae','ben','bhs','bop','bor','bur','pd','vcp','pw','pwg','bop','gst','mwe','mw72','sch','shs','stc','yat','wil','skd']
	# Creating base ngrams
	# '../../../Cologne_localcopy/skd/skdtxt/skd.txt' for SKD and '../../../Cologne_localcopy/vcp/vcptxt/vcp.txt' for VCP.
	indict = sys.argv[1].lower()
	testdict = sys.argv[2].lower()
	if not (indict in handleddictlist and testdict in handleddictlist):
		print "Dictionary you are trying to work with is not supported as of yet. Sorry for inconvenience. Aborting."
		exit(0)
	basefilename = '../../../Cologne_localcopy/'+indict+'/'+indict+'txt/'+indict+'.txt'
	fin1 = codecs.open(basefilename,'r','utf-8')
	data1 = fin1.read()
	fin1.close()
	print "Scraping words from", basefilename
	basewords = getwords(data1,indict)
	print len(basewords), "Words scraped."
	print "Generating bigrams."
	basebigrams = getngrams(basewords,2)
	print len(basebigrams), "bigrams generated."
	print "Generating trigrams."
	basetrigrams = getngrams(basewords,3) 
	print len(basetrigrams), "trigrams generated."

	testfilename = '../../../Cologne_localcopy/'+testdict+'/'+testdict+'txt/'+testdict+'.txt'
	fin2 = codecs.open(testfilename,'r','utf-8')
	data2 = fin2.readlines()
	fin2.close()
	print "Printing the files with abnormal bigrams and trigrams on screen."
	fout = codecs.open(testdict+'vs'+indict+'errors.txt','w','utf-8')
	counter = 0
	positives = 0
	for line in data2:
		counter += 1
		originalline = line.strip()
		line = line.strip()
		wordinline = getwords(line,testdict,True)
		linebigrams = getngrams(wordinline,2)
		linetrigrams = getngrams(wordinline,3)
		if len(linebigrams.difference(basebigrams)) > 0:
			positives += 1
			print line.encode('utf-8')
			diff = linebigrams.difference(basebigrams)
			print str(counter), diff
			fout.write(originalline+'\n')
			fout.write(str(counter)+':'+','.join(list(diff))+'\n')
		elif len(linetrigrams.difference(basetrigrams)) > 0:
			positives += 1
			print line.encode('utf-8')
			diff1 = linetrigrams.difference(basetrigrams)
			print str(counter), diff1
			fout.write(originalline+'\n')
			fout.write(str(counter)+':'+','.join(list(diff1))+'\n')
	fout.close()
	print str(positives), 'suspicious entries found in', testdict
	