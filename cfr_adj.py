""" cfr_adj.py  Sep 29, 2014
 Oct 17, 2014: Separate collations by dictionary
 Oct 18, 2014: Use 'dictionaries' subdirectory. 
      Put correction forms in dictionaries/X/ directory
 Usage: python cfr_adj.py cfr.tsv correctionform.txt
  Note: cfr.tsv is created from Google Spreadsheet
        'Sanskrit-Lexicon Correction form (Responses)'
        by 'File/Download as tab-separated values'
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
   out = "Error 1 for line %s:\n%s" %(n,line)
   print out
   exit(1)
  self.time = oneline(parts[0])
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
 recs=[]
 dictmap = {}
 for line in f:
  line = line.rstrip('\r\n')
  n = n + 1
  rec = CFR(line,n)
  if n == 1:
   hrec = rec
   continue
  recs.append(rec)
  d = rec.dict
  if d not in dictmap:
   dictmap[d] = []
  dictmap[d].append(rec)
 f.close()

 knowndicts = ["AE","AP","AP90","BEN","BHS","BOR","BUR","CAE","CCS",
  "GRA","MW","MW72","PUI","PW","PWG",
  "SCH","SHS","SKD","STC","VCP","VEI","WIL","GST","PD","MD",
  "MCI","YAT","MWE","INM","IEG","PE","ACC"]

 npending = generate_output("ALL",fileout,recs)
 print n,"lines read from",filein
 print npending,"cases are pending"

 for d in dictmap:
  if d not in knowndicts:
   out = "UNKNOWN DICTIONARY: %s %s" %(d,len(dictmap[d]))
   print out.encode('utf-8')
  else:
   generate_output(d,fileout,recs)

#-----------------------------------------------------
if __name__=="__main__":
 filein = sys.argv[1]
 fileout = sys.argv[2]
 adjust(filein,fileout)
