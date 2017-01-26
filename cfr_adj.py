""" cfr_adj.py  Sep 29, 2014
 Oct 17, 2014: Separate collations by dictionary
funderburkjim@gmail.com Oct 18, 2014: Use 'dictionaries' subdirectory. 
      Put correction forms in dictionaries/X/ directory
 Usage: python cfr_adj.py cfr.tsv correctionform.txt
  Note: cfr.tsv is created from Google Spreadsheet
        'Sanskrit-Lexicon Correction form (Responses)'
        by 'File/Download as tab-separated values'
 Jul 18, 2015  Sort records by time, since Google doesn't append
   new records from Correction form to the end.
 Aug 2, 2015  Correct construction of sorttime.
"""
import re,sys,os
import codecs

def oneline(x):
 parts = re.split(r'[\r\n]',x)
 y = ' '.join(parts)
 return y

class CFR(object):
 def __init__(self,line,n):
  parts = line.split('\t')
  self.line = line
  self.n = n
  if len(parts)!= 8:
   print "# of tab-parts should be 8, but is",len(parts)
   out = "Error 1 for line %s:\n%s" %(n,line)
   print out.encode('utf-8')
   exit(1)
  self.time = oneline(parts[0])
  # Jul 18, 2015 - Generate a sortable timefield
  # Assume time is mm/dd/yyyy hh:mm:ss
  # Change to yyyymmdd-hh:mm:ss-nnnn  (nnnnnn = self.n)
  try:
   timeparts = re.split(r'[/: ]',self.time)
   mm = int(timeparts[0])
   dd = int(timeparts[1])
   yyyy = int(timeparts[2])
   h = int(timeparts[3])
   m = int(timeparts[4])
   s = int(timeparts[5])
   self.sorttime = "%4d%02d%02d-%02d%02d%02d-%06d" %(yyyy,mm,dd,h,m,s,n)
  except:
   if n != 1:
    print "ERROR time='%s'" % self.time
    print n,line.encode('utf-8')
    print re.split(r'[/: ]',self.time)
    exit()
   else: # case n=1
    (mm,dd,yyyy,h,m,s) = (0,0,0,0,0,0)
    self.sorttime = "%4d%02d%02d-%02d%02d%02d-%06d" %(yyyy,mm,dd,h,m,s,n)
  self.dict = oneline(parts[1])
  if self.dict == "APES":
   self.dict = "AE"
  elif self.dict == "PWG2013":
   self.dict = "PWG"
  self.lnum = oneline(parts[2])
  self.hw = oneline(parts[3])
  self.old = oneline(parts[4])
  self.new = oneline(parts[5])
  self.comment = oneline(parts[6])
  email = oneline(parts[7])
  self.email = email
  eparts = email.split(r':')
  if eparts >= 2:
   self.user = eparts[0]
   self.status = ':'.join(eparts[1:])
  else:
   self.user = email
   self.status = ''
  self.user = self.user.strip()
  #if self.user == '':
  # self.user='NONE'
  self.useradj = re.sub(r'@.*$','',self.user)
  
 def listform(self):
   return [self.time,self.dict,self.lnum,self.hw,self.old,self.new,self.comment,self.useradj,self.status]

def outputrec(rec,i):
 outar=[]
 (date,time) = rec.time.split(' ')
 out = "Case %s: %s dict=%s, L=%s, hw=%s, user=%s" %(
   rec.n,date,rec.dict,rec.lnum,rec.hw,rec.useradj)
 outar.append(out)
 outar.append("old = %s" % rec.old)
 outar.append("new = %s" % rec.new)
 if rec.comment != 'Typo':
  outar.append('comment = %s' % rec.comment)
 if rec.status == '':
  rec.status = 'PENDING'
 outar.append('status = %s' % rec.status)
 outar.append('-'*72)
 outar.append('')
 return outar

def generate_output(dcode,filename,recs):
 allarr =[] # array of all output lines
 if dcode == "ALL":
  out = "Sanskrit Lexicon Correction Form History"
 else:
  out = "Sanskrit Lexicon Correction Form History for %s" % dcode
 allarr.append(out)
 import datetime
 today = datetime.date.today()
 date = today.strftime("%B %d, %Y")
 out = "As of %s" % date 
 allarr.append(out)
 idxpending = len(allarr) # prepare place-holder
 allarr.append("DUMMY") 
 allarr.append("")
 #fout.write("%s\n" % out)
 #fout.write("\n")
 m = len(recs)
 npending=0
 nfound = 0
 # recs is in ascending order of sorttime.  Read array backwards
 # so new data at the top.
 for i in xrange(m-1,-1,-1):
  rec = recs[i]
  if not (dcode in ['ALL',rec.dict]):
   continue
  nfound = nfound + 1
  outar = outputrec(rec,i)
  for out in outar:
   allarr.append(out)
   if out == 'status = PENDING':
    npending=npending + 1
 # Fill allarr[idxpending]
 allarr[idxpending]="%s correction records, with %s PENDING" %(nfound,npending)
 # generate fileout from dcode and filename
 if dcode == "ALL":
  fileout = filename
 else:
  dir = "%s/%s" %("dictionaries",dcode)
  fileout = "%s/%s_%s" %(dir,dcode,filename)
  if not os.path.isdir(dir):
   if os.path.exists(dir):
    print "ERROR: %s exists, but is not a directory" % dir
    exit(1)
   os.mkdir(dir,0755)
 fout = codecs.open(fileout,'w','utf-8')
 for out in allarr:
  fout.write("%s\n" % out)
 fout.close()
 return npending

def adjust(filein,fileout):
 f = codecs.open(filein,'r','utf-8')
 n = 0
 recsin=[]
 dictmap = {}
 for line in f:
  line = line.rstrip('\r\n')
  n = n + 1
  rec = CFR(line,n)
  if n == 1:
   hrec = rec
   continue
  recsin.append(rec)
  d = rec.dict
  if d not in dictmap:
   dictmap[d] = []
  dictmap[d].append(rec)
 f.close()

 # sort recsin in order of sorttime
 recs=sorted(recsin,key = lambda rec:rec.sorttime)
 # change 'n' based on sort order
 for j in xrange(0,len(recs)):
  rec = recs[j]
  out = "%s,%s,%s" %(rec.sorttime,rec.n,rec.lnum)
  rec.case = rec.n  # new
  rec.n = j+1
 knowndicts = ["AE","AP","AP90","BEN","BHS","BOR","BUR","CAE","CCS",
  "GRA","MW","MW72","PUI","PW","PWG",
  "SCH","SHS","SKD","STC","VCP","VEI","WIL","GST","PD","MD",
  "MCI","YAT","MWE","INM","IEG","PE","ACC","BOP","KRM"]

 npending = generate_output("ALL",fileout,recs)
 print n,"lines read from",filein
 print npending,"cases are pending"
 #print "dbg exiting early"
 for d in dictmap:
  d = d.upper() # Jan 25, 2017
  if d not in knowndicts:
   out = "UNKNOWN DICTIONARY: %s %s" %(d,len(dictmap[d]))
   print out.encode('utf-8')
   m = len(recs)
   print "DBG: m=",m
   for i in xrange(0,m):
    rec = recs[i]
    if rec.dict == d:
     outar=outputrec(rec,i)
     for out in outar:
      print out.encode('utf-8')
  else:
   generate_output(d,fileout,recs)

#-----------------------------------------------------
if __name__=="__main__":
 filein = sys.argv[1]
 fileout = sys.argv[2]
 adjust(filein,fileout)
