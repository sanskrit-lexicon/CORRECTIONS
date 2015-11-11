""" generate.py
 For PW Abbreviation corrections.
 Generate update records for headwords
 Also, generate tsv for correction form responses
 Dhaval modified ejf's Dec 18, 2014 code for the present purpose on November 11, 2015.
 Usage:
 Copy and paste change.txt file after corrections in the present folder and run the below code.
 python generate.py change.txt ../../../orig/pw.txt ../../pwhw2.txt pwabbrvupd.txt pwabbrvupd.tsv 
 Reads 4 items  as number old -> new (old, new in slp1)
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
 def __init__(self,year,minutes,user):
  self.year = year
  self.minutes = minutes
  self.user = user
  self.timestamp = "%s %s" %(self.year,self.minutes)
  self.email = "%s: Corrected %s" %(self.user,self.year)

def correctiontype(text):
	if text == "":
		output = "no change"
	elif text == "p":
		output = "print error"
	elif text == "l":
		output = "lexicographer error"
	elif text == "d":
		output = "digitization error"
	elif text == "o":
		output = "ocr error"
	else:
		output = "no change"
	return output

  
def make_update(inrecs,hwrecs,fileout,filetsv,parms):
 fout = codecs.open(fileout,'w','utf-8')
 ftsv = codecs.open(filetsv,'w','utf-8')

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
  print hw
  """if hw not in hwrecdict:
   out = "HW NOT FOUND: %s" % inrec.line
   print out.encode('utf-8')
   continue"""
  hw1 = inrec.new
  key1 = inrec.key1
  corrtype = correctiontype(inrec.corrtype)
  #print [members.digitization for members in hwrecdict[key1]]
  recs = hwrecdict[key1]
  rec = recs[0] # first one  
  if len(recs) > 1:
   if hw == 'snuta':
    rec = recs[1]
    out = "Correcting 2nd homonym: %s" % inrec.line
    print out.encode('utf-8')
   else: 
    out = "HOMONYMS FOUND: %s" % inrec.key1
    print out.encode('utf-8')
  L = rec.n  # probable 'L'
  nout = nout + 1
  old = rec.digitization
  lnum = rec.linenum1
  new = re.sub(hw,hw1,old)
  if (new == old) and (hw == "aDostrapitta"):
   new = re.sub("aDo'strapitta","aDo'srapitta",old)
  if new == old:
   out = "CORRECTION NOT MADE: %s" % inrec.key1
   print out.encode('utf-8')
   out = '; %s PW Abbrv correction %s %s -> %s TODO\n' % (parms.year,corrtype,hw,hw1)
   continue
  else:
   out = '; %s PW Abbrv correction %s %s -> %s\n' % (parms.year,corrtype,hw,hw1)
  fout.write(out)
  out = "%s old %s\n" %(lnum,old)
  fout.write(out)
  out = "%s new %s\n" %(lnum,new)
  fout.write(out)
  # generate tsv output
  outarr=[]
  outarr.append(parms.timestamp) 
  outarr.append('PW')
  outarr.append('%s' %L) # L
  outarr.append(hw) # Headword
  outarr.append(hw) # old
  
  outarr.append(hw1) # new
  outarr.append(corrtype)
  outarr.append(parms.email)
  out = '\t'.join(outarr)
  ftsv.write('%s\n' % out)
 # close output
 fout.close()
 ftsv.close()
 # informational message
 print nout,"Changes written to ",fileout
 print nout,"Correction form responses written to ",filetsv

class Input(object):
 def __init__(self,line):
  line = line.rstrip('\r\n')
  line = line.rstrip() # remove trailing blanks
  self.line = line # the text
  parts = re.split(r'[;@]+',line)
  try:
   (self.id,self.old,self.new,self.key1,self.corrtype) = (parts[-1],parts[2],parts[1],parts[-4],parts[0])
  except:
   print "Input ERROR: Wrong # of parts: %s" % len(parts)
   for i in xrange(0,len(parts)):
    out = "part#%s='%s'" %(i+1,parts[i])
    print out.encode('utf-8')
   exit(1)
  self.hwrec = None # filled in later

if __name__=="__main__":
 fileinrec = sys.argv[1] 
 with codecs.open(fileinrec,encoding='utf-8',mode='r') as f:
  inrecs = [Input(line) for line in f if (not line.startswith(';'))]
 filein = sys.argv[2] # pw.txt
 filein1 = sys.argv[3] # pwhw2.txt
 fileout = sys.argv[4] #
 filetsv = sys.argv[5] #
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
 parms = Parms(date,time,"Dhaval")
 print "parms=",(parms.year,parms.minutes,parms.user)
 
 make_update(inrecs,hwrecs,fileout,filetsv,parms)

