# coding=utf-8

""" cfr_adj1.py adapated from csl-corrections/cfr_adj.py
"""
from __future__ import print_function
import re,sys,os
import codecs

def write_lines(fileout,outarr,printFlag=False):
 with codecs.open(fileout,"w","utf-8") as f:
  for out in outarr:
   f.write(out+'\n')
 if printFlag:
  print(len(outarr),"lines written to",fileout)

def oneline(x):
 parts = re.split(r'[\r\n]',x)
 y = ' '.join(parts)
 return y

class CFR(object):
 def __init__(self,line,n):
  parts = line.split('\t')
  self.line = line
  self.n = n
  self.inputstatus = True
  if len(parts)!= 8:
   print("# of tab-parts should be 8, but is",len(parts))
   out = "Error 1 for line %s:\n%s" %(n,line)
   print(out)
   self.inputstatus = False
   return
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
    print("ERROR time='%s'" % self.time)
    self.inputstatus = False
    return
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
  self.email = email.rstrip()
  eparts = email.split(r':')
  if len(eparts) >= 2:
   self.user = eparts[0]
   self.status = ':'.join(eparts[1:])
  else:
   self.user = email
   self.status = ''
  self.user = self.user.strip()
  self.useradj = re.sub(r'@.*$','',self.user)
  
 def unused_listform(self):
   return [self.time,self.dict,self.lnum,self.hw,self.old,self.new,self.comment,self.useradj,self.status]

def outputrec(rec,i):
 outar=[]
 if rec.inputstatus == False:
  out = "Case %s: BAD INPUT: %s" %(i,rec.line)
  outar.append(out)
  outar.append('-'*72)
  outar.append('')
  return outar
 # (date,time) = rec.time.split(' ')
 #out = "Case %s: %s dict=%s, L=%s, hw=%s, user=%s" %(
 #  rec.n,rec.time,rec.dict,rec.lnum,rec.hw,rec.useradj)
 outar.append('Case %s: %s' % (rec.n,rec.time))
 outar.append("dict=%s, L=%s, hw=%s, user=%s" %
               (rec.dict,rec.lnum,rec.hw,rec.useradj))
 #outar.append(out)
 #outar.append(out)
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
 print('generate_outputL dcode=%s, #recs=%s' %(dcode,len(recs)))
 allarr.append('User corrections %s' % filename)
 allarr.append('')
 m = len(recs)
 npending=0
 nfound = 0
 for i,rec in enumerate(recs):
  rec = recs[i]
  nfound = nfound + 1
  outar = outputrec(rec,i)
  for out in outar:
   allarr.append(out)
 write_lines(filename,allarr,printFlag=True)
 return npending


def adjust(filein,fileout):
 f = codecs.open(filein,'r','utf-8')
 n = 0
 recsin=[]
 dictmap = {}
 for iline,line in enumerate(f):
  line = line.rstrip('\r\n')
  n = n + 1
  rec = CFR(line,n)
  recsin.append(rec)
 f.close()
 recs = recsin
 generate_output("ALL",fileout,recs)

#-----------------------------------------------------
if __name__=="__main__":
 filein = sys.argv[1]
 fileout = sys.argv[2]
 adjust(filein,fileout)
