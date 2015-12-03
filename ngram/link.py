# -*- coding: utf-8 -*-
""" Give webpage links and PDF links to the standard convention.

See https://github.com/sanskrit-lexicon/CORRECTIONS/issues/154#issuecomment-161526829 for standard convention.
  
Usage -

python link.py inputfile outputfile HTMLheading repositoryname issuenumber

e.g.

python link.py output/allvsMW_1.txt output/html/allvsMW_1.html 1gramwords CORRECTIONS 185
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

header = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html><head><style>table, td, th {border:1px solid black; padding: 10px;}</style><!--... Defining UTF-8 as our default character set, so that devanagari is displayed properly. --><meta charset="UTF-8"></head><body>';

def pdflink(word,dict):
	if word == '-':
		return '-'
	else:
		return '<a href="http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict='+dict+'&key='+word+'" target="_blank">'+dict+'</a>'
def colognehrefyear(dict):
	dictionaryname = ["ACC","CAE","AE","AP90","AP","BEN","BHS","BOP","BOR","BUR","CCS","GRA","GST","IEG","INM","KRM","MCI","MD","MW72","MW","MWE","PD","PE","PGN","PUI","PWG","PW","SCH","SHS","SKD","SNP","STC","VCP","VEI","WIL","YAT"]
	hrefyear = ["2014","2014","2014","2014","2014","2014","2014","2014","2014","2013","2014","2014","2014","2014","2013","2014","2014","2014","2014","2014","2013","2014","2014","2014","2014","2013","2014","2014","2014","2013","2014","2013","2013","2014","2014","2014"]
	ans = '?'
	for i in xrange(len(dictionaryname)):
		if dict == dictionaryname[i]:
			ans = hrefyear[i]
			break
	return ans
def webpagelink(dict,word):
	y = colognehrefyear(dict)
	if word == '-':
		return '-'
	else:
		return '<a href="http://www.sanskrit-lexicon.uni-koeln.de/scans/'+dict+'Scan/'+y+'/web/webtc/indexcaller.php?key='+word+'&input=slp1&output=SktDevaUnicode" target="_blank">'+word+'</a>';
def highlightdiff(word,substring):
	highlightstyle = '<b style="background-color:#ccffcc">$new_diff</b>'
	location = word.find(substring)
	return word[:location] + '<b style="background-color:#ffff00">' + substring + '</b>' + word[location+len(substring):]
def webpagelink1(dict,word,diff):
	y = colognehrefyear(dict)
	if word == '-':
		return '-'
	else:
		return '<a href="http://www.sanskrit-lexicon.uni-koeln.de/scans/'+dict+'Scan/'+y+'/web/webtc/indexcaller.php?key='+word+'&input=slp1&output=SktDevaUnicode" target="_blank">'+highlightdiff(word,diff)+'</a>';
def linking(fin,fout,issuedescription,reponame,issuenumber):
	global header
	infile = codecs.open(fin,'r','utf-8')
	input = infile.readlines()
	input = triming(input)
	outfile = codecs.open(fout,'w','utf-8')
	outfile.write(header)
	outfile.write('<h1>'+issuedescription+' (See <a href="https://github.com/sanskrit-lexicon/'+reponame+'/issues/'+issuenumber+'">This issue</a>)</h1>')
	outfile.write('<p>Help us speed up corrections by submitting corrections in <a href="https://github.com/sanskrit-lexicon/CORRECTIONS/issues/154#issue-116719290">Standard convention</a></p>')
	counter = 1
	outfile.write('<table><tr><th>Sr</th><th>Dict</th><th>L-id</th><th>Wegpage</th><th>PDF</th><th>Webpage</th><th>PDF</th><th>Notes</th></tr>\n')
	for member in input: #sch:akLpta:akLpta:n:173#Lp,kL
		split = member.split(':')
		dict = split[0].upper()
		wrongword = split[1]
		errortype = split[3]
		if not errortype == 'n':
			rightword = split[2]
		else:
			rightword = '-'
		notes = split[4]
		lnum = '-'
		if re.search('#',notes):
			[notes,lnum] = notes.split('#')
			note = notes.split(',')[0]
		#outfile.write('<tr><td>'+str(counter)+'</td><td>'+dict.upper()+'</td><td>'+lnum+'</td><td>'+webpagelink(dict,wrongword)+'</td><td>'+pdflink(wrongword,dict)+'</td><td>'+webpagelink(dict,rightword)+'</td><td>'+pdflink(rightword,dict)+'</td><td>'+notes+'</td></tr>\n')
		outfile.write('<tr><td>'+str(counter)+'</td><td>'+dict.upper()+'</td><td>'+lnum+'</td><td>'+webpagelink1(dict,wrongword,note)+'</td><td>'+pdflink(wrongword,dict)+'</td><td>'+webpagelink1(dict,rightword,note)+'</td><td>'+pdflink(rightword,dict)+'</td><td>'+notes+'</td></tr>\n')
		counter += 1
	outfile.write('</table></body></html>')
	outfile.close()
	print "Check", fout, "for testing"

if __name__=="__main__":
	fin = sys.argv[1]
	fout = sys.argv[2]
	issuedescription = sys.argv[3]
	reponame = sys.argv[4]
	issuenumber = sys.argv[5]
	linking(fin,fout,issuedescription,reponame,issuenumber)
	