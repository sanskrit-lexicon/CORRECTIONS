import sys, re
import codecs
import string
import datetime

correctionforms = codecs.open('../correctionform.txt','r','utf-8')
# Function to return timestamp
def timestamp():
	strtime = datetime.datetime.now()
	strtime = str(strtime)
	(date, time) = strtime.split(' ')
	return (date, time)
def striping(text):
	text = text.strip('\r\n')
	return text.strip('\r\n')
def stripold(text):
	text = text.lstrip("old = ")
	return text.strip()
# See http://stackoverflow.com/questions/6486450/python-compute-list-difference
def diff(a,b):
	b = set(b)
	return [aa for aa in a if aa not in b]
def unique(a):
	output = []
	for aa in a:
		if aa not in output:
			output.append(aa)
	return output
def sanhw1():
	infile = codecs.open('../sanhw1/sanhw1.txt','r','utf-8')
	output = []
	for line in infile:
		cleanline = line.strip()
		word = cleanline.split(':')[0]
		output.append(word)
	return output
sanhw1 = sanhw1()
def sanhw2():
	infile = codecs.open('../sanhw2/sanhw2.txt','r','utf-8')
	output = []
	for line in infile:
		cleanline = line.strip()
		word = cleanline.split(':')[0]
		output.append(word)
	return output
sanhw2 = sanhw2()

def correctedentries():
	global correctionforms
	correctedwords = codecs.open('correctedwords.txt','w','utf-8')
	separator = "------------------------------------------------------------------------"
	data = correctionforms.read()
	eachentry = data.split(separator)
	eachentry = map(striping,eachentry)
	print "There are %s entries in correctionforms.txt" % len(eachentry)
	output = []
	for entry in eachentry:
		lines = entry.split("\r\n")
		if len(lines)==4 and ("status =  Corrected" in lines[3] or "status =  Cprrected" in lines[3]):
			output.append(stripold(lines[1]))
			correctedwords.write(stripold(lines[1])+"\n")
		elif len(lines)==5 and ("status =  Corrected" in lines[4] or "status =  Cprrected" in lines[4]):
			output.append(stripold(lines[1]))			
			correctedwords.write(stripold(lines[1])+"\n")
	print "There are %s entries which have been corrected" % len(output)
	
	return output
correcteds = correctedentries()

# inputfile is the file which was examined for errors.
# filetype is 1 - for file like https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/MWvsOthers/MWagainstPWG.html
# filetype is 2 - for file like https://github.com/sanskrit-lexicon/CORRECTIONS/blob/master/nochange/testedfiles/hiatusmw.txt
def readinputfile(inputfile,filetype):
	input = codecs.open(inputfile,'r','utf-8')
	data = input.read()
	wordsexamined = []
	if filetype == 1:
		data = data.strip("<br>")
		entries = data.split('<br>')
		for entry in entries:
			entry = entry.strip()
			if '<b 'not in entry and entry.startswith('<a '):
				reg = r'[>]([a-zA-Z]+)\b'
				m = re.split(reg,entry)
				wordsexamined.append(m[1].strip())
		return wordsexamined
	elif filetype == 2:
		data = data.strip()
		entries = data.split('\n')
		for entry in entries:
			wordsexamined.append(entry.split(',')[0])
		return wordsexamined
	else:
		print "Filetype error"
		exit(1)
	
# inputfile is the file which was examined for errors.
# filetype is 1 - for file like https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/MWvsOthers/MWagainstPWG.html
# issuenumber is the issue number in CORRECTIONS repository.
def nochangescraper(inputfile,filetype,issuenumber,dictcode):
	global correcteds, sanhw1
	inputfile = "testedfiles/"+inputfile
	outfilename = "nochange_issue_"+str(issuenumber)+".txt"
	nochangetxt = codecs.open(outfilename,'w','utf-8')
	wordsexamined = readinputfile(inputfile,filetype)
	nochangelist = diff(wordsexamined,correcteds)
	for mem in nochangelist:
		if mem in sanhw1:
			nochangetxt.write(mem+":"+dictcode+"\n")
	print "wrote %s no change headwords to nochange_issue_%s.txt file, %s dictionary" % (len(nochangelist),issuenumber,dictcode)
	print 
	nochangetxt.close()
		
# This is a list containing tuples (filename,filetype,issuenumber,dictcode) entries.
testedfiles = [('MWagainstPWG.html',1,2,'MW'),('PWKvsMW.html',1,8,'PW'),('hiatusmw.txt',2,10,'MW'),('MWvsVCP.html',1,21,'MW'),('VCPvsMW.html',1,32,'VCP'),('VCPvsPW.html',1,36,'VCP')]
#testedfiles = [('VCPvsPW.html',1,36,'VCP')]
for (a,b,c,d) in testedfiles:
	nochangescraper(a,b,c,d)
