""" generate.py
 For Correction of composite HTML files. See issue 155.
 Generate update records for headwords
 Also, generate tsv for correction form responses
 Dhaval modified ejf's Dec 18, 2014 code for the present purpose on November 13, 2015.
 Usage:
 Copy and paste change.txt file after corrections in the present folder and run the below code.
 Either run `prepareupd.sh` for all dictionaries or 
 `python generate.py change.txt ../../../../"$VALUE"/"$VALUE"txt/"$VALUE".txt ../../../../"$VALUE"/"$VALUE"xml/xml/"$VALUE"hw2.txt upd/"$VALUE"abbrvupd.txt upd/"$VALUE"abbrvupd.tsv upd/"$VALUE"nochange.txt $VALUE` for specific dictionary.
 where $VALUE is the dictionary code.
 Reads 4 items  as number old -> new (old, new in slp1)
 
 Presumptions -
 1. All dictionaries are placed in cologne directory. e.g. cologne/pw
 2. Every dictionary (e.g. cologne/pw) has the following subdirectories (1) DICTCODEtxt (pwtxt), (2) DICTCODEweb1 (pwweb1) and (3) DICTCODExml (pwxml).
 3. DICTCODEtxt folder has DICTCODE.txt file (e.g. cologne/pw/pwtxt has pw.txt).
 4. DICTCODExml/xml folder has DICTCODEhw2.txt file (e.g. cologne/pw/pwxml/xml has pwhw2.txt file)
 5. Current code i.e. generate.py, change.txt and prepareupd.sh are placed in cologne/pw/pywork/correctionwork/correction-issue-155 folder.
 5. All these directories are downloadable from cologne dictionary download page.
 
 Outupt -
 1. They are stored in cologne/pw/pywork/correctionwork/correction-issue-155/upd folder.
 2. For each dictionary we generate three files. (1) DICTCODEupd.txt for copy pasting to manualByLine02.txt. (2) DICTCODEupd.tsv, a tab separated file having the same fields. (3) DICTCODEnochange.txt - file storing no change cases. 
 3. There are three composite files also (1) allchangeupd.txt (2) allchangeupd.tsv and (3) allnochange.txt files which have entries of all dictionaries.
  
"""
import sys, re
import codecs
import string
import datetime

# Function to return timestamp
def timestamp():
	strtime = datetime.datetime.now()
	strtime = str(strtime)
	(date, time) = strtime.split(' ')
	return (date, time)
tranfrom="aAiIuUfFxXeEoOMHkKgGNcCjJYwWqQRtTdDnpPbBmyrlvSzsh"
tranto = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvw"
trantable = string.maketrans(tranfrom,tranto)
def slp_cmp(a,b):
 a1 = string.translate(a,trantable)
 b1 = string.translate(b,trantable)
 return cmp(a1,b1)

class Vrec(object):
 def __init__(self,line,page,colline,n):
  self.line = line # the text
  self.page = page # the page (a string)
  self.col =  ''  # No column. The col within page (a string)
  self.colline = colline # the line number within the column of the page.
  self.n = n # integer line number within file (starting at 1)

def alphaerr_lineP(x):
 if '{??}' in x:
  return True
 return False

def unused_init_vrecs(filein):
 vrecs = [] 
 f = codecs.open(filein,encoding='utf-8',mode='r')
 rePage = re.compile(r"\[Page(.*?)\]")
 n = 0 # count of lines in file
 page = None # will be adjusted 
 for line in f:
  line = line.strip()
  n = n + 1
  if (n > 5000000):
   print "dbg: init_vrecs: stopping after %s lines"%n
   return vrecs
  pages = rePage.findall(line)
  if len(pages) == 0:
   colline = colline + 1
   vrec = Vrec(line,page,colline,n)
   vrecs.append(vrec)
   continue
  # case where this line has a 'Page' designation 
  # add this vrec with PREVIOUS page, col info
  if n == 1:
   #special situation of first line in file
   # there is no previous info. So dream some up
   page = '0001'
   colline = 0 # only case where this is in vrec
   vrec = Vrec(line,page,colline,n)
   vrecs.append(vrec)
  else:
   colline = colline + 1 # incr. colline
   vrec = Vrec(line,page,colline,n) # use prior page,col
   vrecs.append(vrec)
  # now, initialize page,colline for next record
  pagelast = pages[-1] # last match
  m = re.match(r'^([0-9]+)',pagelast)
  if m:
   page = m.group(1) # vol-ppp
   col = '' # may be blank. Just skip this?
  colline = 0 # start this counter  
 return vrecs

class Hwrec(object):
 def __init__(self,line,n):
  line = line.rstrip('\r\n')
  self.line = line # the text
  self.n = n # integer line number within file (starting at 1)
  (self.pageref,self.hwslp,self.linenum12) = re.split(r':',line)
  # next required for use in slp_cmp
  (self.linenum1,self.linenum2) = re.split('[,]',self.linenum12)
  self.digitization = None # to be filled later
def init_hwrecs(filein):
 #f = codecs.open(filein,encoding='utf-8',mode='r')
 # filein is ascii file (pwhw2.txt)
 # read it as Ascii so slp_cmp string.translate works
 f = codecs.open(filein,mode='r') 
 recs = [] 
 n = 0 # count of lines in file
 for line in f:
  n = n + 1
  recs.append(Hwrec(line,n))
 f.close()
 return recs

class Parms(object):
 def __init__(self,year,minutes,user,issuenumber):
  self.year = year
  self.minutes = minutes
  self.user = user
  self.timestamp = "%s %s" %(self.year,self.minutes)
  self.email = "%s: Corrected %s" %(self.user,self.year)
  self.issuenumber = issuenumber

def correctiontype(text):
	if text == "p":
		output = "print error"
	elif text == "l":
		output = "lexicographer error"
	elif text == "d":
		output = "digitization error"
	elif text == "o":
		output = "ocr error"
	elif text == "m":
		output = "miscellaneous error"
	elif text == "n":
		output = "no change"
	elif text == "s":
		output = "separate words"
	elif text == "a":
		output = "alternate words"
	elif text == "w":
		output = "wrong reading"
	elif text == "":
		output = "pending"
	return output

  
def make_update(inrecs,hwrecs,fileout,filetsv,filenochange,parms,dict):
 fout = codecs.open(fileout,'w','utf-8')
 ftsv = codecs.open(filetsv,'w','utf-8')
 fnoch = codecs.open(filenochange,'w','utf-8')
 global allchangefile, allchangetsv, allnochangefile 
 # make dictionary of hwrecs. Allow for homonyms
 hwrecdict = {}
 for rec in hwrecs:
  hw = rec.hwslp
  if hw not in hwrecdict:
   hwrecdict[hw]=[]
  hwrecdict[hw].append(rec)
 # read inrecs, and generate output
 n = 0 # count of lines read
 lnum = 0 # generate record number for xml records constructed
 nout = 0
 for inrec in inrecs:
  hw = inrec.old
  hw1 = inrec.new
  key1 = inrec.old
  corrtype = correctiontype(inrec.corrtype)
  note = inrec.note
  #print [members.digitization for members in hwrecdict[key1]]
  if key1 in hwrecdict:
   recs = hwrecdict[key1]
   rec = recs[0] # first one
  else:
   continue
  if len(recs) > 1:
   if hw == 'snuta':
    rec = recs[1]
    out = "Correcting 2nd homonym: %s" % inrec.line
    print out.encode('utf-8')
   else: 
    out = "HOMONYMS FOUND: %s" % key1
    print out.encode('utf-8')
  L = rec.n  # probable 'L'
  old = rec.digitization
  lnum = rec.linenum1
  new = re.sub(hw,hw1,old)
  if inrec.corrtype in ["p","o","l","d","m"]:
   if (new == old) and (hw == "aDostrapitta"):
    new = re.sub("aDo'strapitta","aDo'srapitta",old)
   if new == old:
    out = "CORRECTION NOT MADE: %s" % inrec.key1
    print out.encode('utf-8')
    out = '; %s, Issue %s, Case %s, User %s, %s\n; %s -> %s # %s # %s TODO\n' % (dict,parms.issuenumber,nout,parms.user,parms.year,hw,hw1,corrtype,note)
    continue
   else:
    nout = nout + 1
    out = '; %s, Issue %s, Case %s, User %s, %s\n; %s -> %s # %s # %s\n' % (dict,parms.issuenumber,nout,parms.user,parms.year,hw,hw1,corrtype,note)
    out += "%s old %s\n" %(lnum,old)
    out += "%s new %s\n" %(lnum,new)
    fout.write(out)
    allchangefile.write(out)
    outtsv = '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (dict,parms.issuenumber,nout,parms.user,parms.year,hw,hw1,corrtype,note,lnum,old,new)
    ftsv.write('%s\n' % outtsv)
    allchangetsv.write('%s\n' % outtsv)
  elif inrec.corrtype in ["n","s","a","w"]:
   out = "%s:%s:%s:%s:%s" % (dict,hw,hw1,corrtype,note)
   fnoch.write(out+"\n")
   allnochangefile.write(out+"\n")
 # close output
 fout.close()
 ftsv.close()
 fnoch.close()
 # informational message
 print nout,"Changes written to ",fileout
 print nout,"Correction form responses written to ",filetsv

class Input(object):
 def __init__(self,line):
  line = line.rstrip('\r\n')
  line = line.rstrip() # remove trailing blanks
  self.line = line # the text
  #parts = re.split(r'[:]+',line)
  parts = line.split(':')
  if parts[3] is not "":
   (self.dictname,self.old,self.new,self.corrtype,self.note) = (parts[0],parts[1],parts[2],parts[3],parts[4])
  else:
   print "Input ERROR: Wrong # of parts: %s" % len(parts)
   for i in xrange(0,len(parts)):
    out = "part#%s='%s'" %(i+1,parts[i])
    print out.encode('utf-8')
   exit(1)
  self.hwrec = None # filled in later

def keeponlyproperdicts(changefile,dict):
	output = []
	f = codecs.open(changefile,'r','utf-8')
	for line in f:
		parts = line.split(':')
		if parts[0] == dict:
			output.append(line)
	return output

if __name__=="__main__":
 fileinrec = sys.argv[1] 
 filein = sys.argv[2] # pw.txt
 filein1 = sys.argv[3] # pwhw2.txt
 fileout = sys.argv[4] #
 filetsv = sys.argv[5] #
 filenochange = sys.argv[6]
 allchangefile = codecs.open('upd/allchangeupd.txt','a','utf-8')
 allchangetsv = codecs.open('upd/allchangeupd.tsv','a','utf-8')
 allnochangefile = codecs.open('upd/allnochange.txt','a','utf-8')
 dict = sys.argv[7]
 inrecs = [Input(line) for line in keeponlyproperdicts(fileinrec,dict)]
 # slurp vcphw2.txt  into Hwrec objects
 hwrecs = init_hwrecs(filein1)
 # slurp vcp.txt into array of lines
 vrecs = []
 with codecs.open(filein,'r','utf-8') as f:
  vrecs=[line.rstrip('\r\n') for line in f]
 # put the first line in vrecs into hwrec records
 for hwrec in hwrecs:
  n1 = int(hwrec.linenum1) - 1
  line = vrecs[n1]
  hwrec.digitization = line
 # Generate timestamp
 (date, time) = timestamp()
 parms = Parms(date,time,"Dhaval","155")
 print "parms=",(parms.year,parms.minutes,parms.user)
 
 make_update(inrecs,hwrecs,fileout,filetsv,filenochange,parms,dict)

