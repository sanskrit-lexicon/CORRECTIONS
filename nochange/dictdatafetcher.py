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

def reginarray(hw,sanhw1withdict):
	matching = [s for s in sanhw1withdict if s.startswith(hw+":")]
	return matching[0].strip()

# version is 0 for nochange0.txt - Only headwords
# version is 1 for nochange1.txt - headwords + dictcodes
# version is 2 for nochage2.txt - headwords + dictcodes with L numbers
def nochangecomposite(inputfile,outfile,version):
	with open(inputfile) as f:
		data = f.readlines()
	f.close()
	print "Total of %s entries to be examined from %s.\nBe patient" % (len(data),inputfile)
	counter = 0
	entered = 0
	for line in data:
		line = line.strip()
		if version == 0:
			outfile.write(line+"\n")
			entered += 1
		elif version == 1:
			outfile.write(reginarray(line,sanhw1withdict)+"\n")
			entered += 1
		elif version == 2:
			outfile.write(reginarray(line,sanhw2withdict)+"\n")
			entered += 1
		counter += 1
		if counter % 100 == 0:
			print "%s / %s entries entered." % (entered,counter)
	print "%s / %s entries entered." % (entered,counter)
	outfile.close()

if __name__=="__main__":
	filein = sys.argv[1] 
	nczero = codecs.open('nc.txt','a','utf-8')
	print "######Generating nc.txt######"
	print 
	nochangecomposite(filein,nczero,0)
	