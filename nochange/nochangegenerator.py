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
def sanhw1withdict():
	infile = codecs.open('../sanhw1/sanhw1.txt','r','utf-8')
	output = []
	for line in infile:
		cleanline = line.strip()
		output.append(line)
	return output
sanhw1withdict = sanhw1withdict()
def sanhw2():
	infile = codecs.open('../sanhw2/sanhw2.txt','r','utf-8')
	output = []
	for line in infile:
		cleanline = line.strip()
		word = cleanline.split(':')[0]
		output.append(word)
	return output
sanhw2 = sanhw2()
def sanhw2withdict():
	infile = codecs.open('../sanhw2/sanhw2.txt','r','utf-8')
	output = []
	for line in infile:
		cleanline = line.strip()
		output.append(line)
	return output
sanhw2withdict = sanhw2withdict()

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
	print 
	return output
correcteds = correctedentries()

def faultfinderhtmlreader(filename):
	fin = codecs.open(filename,'r','utf-8')
	data = fin.read()
	body = data.split('<body>')[1]
	body = body.strip('</body></html>')
	entries = body.split('</br>')
	output = []
	for entry in entries:
		parts = entry.split(' - ')
		hw = parts[0].strip()
		output.append(hw)
	return output
# inputfile is the file which was examined for errors.
# filetype is 1 - for file like https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/MWvsOthers/MWagainstPWG.html
# filetype is 2 - for file like https://github.com/sanskrit-lexicon/CORRECTIONS/blob/master/nochange/testedfiles/hiatusmw.txt
# filetype is 3 - for file like https://github.com/sanskrit-lexicon/CORRECTIONS/blob/master/nochange/testedfiles/AllvsMW.html
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
	elif filetype == 3:
		wordsexamined = faultfinderhtmlreader(inputfile)
		return wordsexamined
	else:
		print "Filetype error"
		exit(1)
	
def reginarray(hw,sanhw1withdict):
	matching = [s for s in sanhw1withdict if s.startswith(hw+":")]
	return matching[0].strip()

def postprocessfaultfinder(inputfile,outputfile):
	global sanhw1withdict
	fin = codecs.open(inputfile,'r','utf-8')
	fout = codecs.open(outputfile,'w','utf-8')
	with open(inputfile) as f:
		data = f.readlines()
	out = []
	counter = 0
	print "Bringing the data of Dictionaries alongwith headwords. It may take a lot of time.\nBe patient."
	for line in data:
		hw = line.split(':')[0]
		hw = hw.strip()
		fout.write(reginarray(hw,sanhw1withdict)+"\n")
		counter += 1
		if counter % 100 == 0:
			print "%s / %s words - additions of dictionaries done. Please wait" % (counter,len(data))
	fin.close()

def nochangecomposite(outlist,inputfile,outfile):
	with open(inputfile) as f:
		data = f.readlines()
	fout = codecs.open(outfile,'r','utf-8')
	for line in data:
		line = line.strip()
		if line not in outlist:
			outlist.append(line)
			fout.write(outlist+"\n")

	
# inputfile is the file which was examined for errors.
# filetype is 1 - for file like https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/MWvsOthers/MWagainstPWG.html
# issuenumber is the issue number in CORRECTIONS repository.
def nochangescraper(inputfile,filetype,issuenumber,dictcode):
	global correcteds, sanhw1
	inputfile = "testedfiles/"+inputfile
	outfilename = "output/nc_"+str(issuenumber)+".txt"
	outfilecorrected = "output/nc_dict_"+str(issuenumber)+".txt"
	nochangetxt = codecs.open(outfilename,'w','utf-8')
	wordsexamined = readinputfile(inputfile,filetype)
	nochangelist = diff(wordsexamined,correcteds)
	outlist = []
	print "Total %s entries to be examined from %s.\nBe patient." % (len(nochangelist),inputfile)
	counter = 0
	for mem in nochangelist:
		if mem in sanhw1:
			nochangetxt.write(mem+"\n")
			counter += 1
			if counter % 1000 == 0:
				print "Wrote %s no change headwords to output/nc%s.txt file, %s dictionary" % (counter,issuenumber,dictcode)
	print "Wrote %s no change headwords to output/nc%s.txt file, %s dictionary" % (counter,issuenumber,dictcode)
	nochangetxt.close()
	print 
	print 

# This is a list containing tuples (filename,filetype,issuenumber,dictcode) entries.
testedfiles = [('MWagainstPWG.html',1,2,'MW'),('PWKvsMW.html',1,8,'PW'),('hiatusmw.txt',2,10,'MW'),('MWvsVCP.html',1,21,'MW'),('VCPvsMW.html',1,32,'VCP'),('VCPvsPW.html',1,36,'VCP'),('AllvsMW.html',3,37,'All')]
#testedfiles = [('AllvsMW.html',3,37,'All')]
for (a,b,c,d) in testedfiles:
	nochangescraper(a,b,c,d)

