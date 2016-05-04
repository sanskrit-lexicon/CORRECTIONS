# -*- coding: utf-8 -*-
"""prep1key2.py for skd
  Apr 20, 2016
  ython prep1keys.py skd-only.txt prep1keys.txt
"""
import re
import sys,codecs

def adjust_datalines(dictcode,datalines):
 if dictcode == 'skd':
  # skd has one word per line, usually. fabricate new datalines.
  outlines=[]
  outline=''
  for line in datalines:
   if (len(outline)+len(line)) < 72:
    outline = outline + ' ' + line
   else:
    outlines.append(outline)
    outline = line
  outlines.append(outline)
  datalines = outlines
 return datalines

def disp_org(dictcode,icase,L,hw0,url,page0,datalines):
 """ return array of lines, formatted for details of Emacs org mode
   
 """
 outarr=[]
 pageref = "[[%s][page %s]]" %(url,page0)
 outarr.append('* TODO Case %04d: %s %s ' % (icase,hw0,pageref))
 # construct potential headword change record
 out = ";%s:%s,%s:%s:n:" %(dictcode,hw0,L,hw0)
 outarr.append(out)
 datalines = adjust_datalines(dictcode,datalines)
 # output up to 10 lines of datalines
 outlines = datalines[0:10]
 for x in outlines:
  # Remove '|', which is a line-separator 
  #x = re.sub(r'[|]','',x)
  y = transcoder.transcoder_processString(x,'as','roman')
  outarr.append(';  %s' % y)
 if len(datalines)>10:
  ndiff = len(datalines) - 10
  outarr.append(';   [and %s more lines]' % ndiff)
 outarr.append('')
 return outarr

def disp_md(dictcode,icase,L,hw0,url,page0,datalines):
 """ return array of lines, formatted for details of GitHub Markdown
 """
 outarr=[]
 pageref = "[page %s](%s)" %(page0,url)
 outarr.append(' Case %04d: %s  %s ' % (icase,hw0,pageref))
 datalines = adjust_datalines(dictcode,datalines)
 # output up to 10 lines of datalines
 outlines = datalines[0:10]
 outarr.append('```')
 # construct potential headword change record
 out = "%s:%s,%s:%s:n:" %(dictcode,hw0,L,hw0)
 outarr.append(out)
 outarr.append('')
 for x in outlines:
  # Remove '|', which is a line-separator in SKD
  x = re.sub(r'[|]','',x)
  y = transcoder.transcoder_processString(x,'as','roman')
  if (y.strip() != ''):
   outarr.append('%s' % y)
 if len(datalines)>10:
  ndiff = len(datalines) - 10
  outarr.append('  [and %s more lines]' % ndiff)
 outarr.append('```')
 outarr.append('------------------------------------------')
 outarr.append('')
 return outarr

def main(dictcode,headwords,inlines,hwrecs,fileout1,fileout2):
 f1=codecs.open(fileout1,"w","utf-8")
 f2=codecs.open(fileout2,"w","utf-8")
 nout=0
 d = {}
 for hwrec in hwrecs:
  d[hwrec.hwslp]=hwrec
 for hw in headwords:
  if hw not in d:
   print "Could not find headword",hw
   continue
  hwrec = d[hw]
  datalines = inlines[hwrec.linenum1-1:hwrec.linenum2]
  # is it a foreign word? If so, get list of languages.
  hw0 = hwrec.hwslp
  L = hwrec.lnum
  firstline = datalines[0] 
  page0 = hwrec.pagecol
  l1 = hwrec.linenum1
  l2 = hwrec.linenum2
  wordtype=''
  nout = nout + 1
  icase = nout
  # output to Org mode and Markdown
  baseurl='http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=%s'% dictcode
  url = '%s&page=%s' %(baseurl,page0)
  # org mode
  outarr = disp_org(dictcode,icase,L,hw0,url,page0,datalines)
  f1.write('\n'.join(outarr))
  # markdown
  outarr = disp_md(dictcode,icase,L,hw0,url,page0,datalines)
  f2.write('\n'.join(outarr))
  if (icase == 100) and True:  # dbg
   print "debug",icase
   break
   pass
 f1.close()
 f2.close()
 print nout,"records written to ",fileout1
 print nout,"sections written to ",fileout2

 
class Headword(object):
 def __init__(self,line,n):
  line = line.rstrip('\r\n')
  self.line = line
  self.lnum = n
  (self.pagecol,self.hwslp,linenum12) = re.split('[:]',line)
  (linenum1,linenum2) = re.split(r',',linenum12)
  self.linenum1=int(linenum1)
  self.linenum2=int(linenum2)

def init_headwords(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  recs = []
  lnum=0
  for x in f:
   lnum = lnum+1
   recs.append(Headword(x,lnum))
 return recs

def init_nochangekeys(filein):
 # slurp filein into dictionary of headwords.
 d = {} # returned dictionary. Value is True always. Could use a set
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  for x in f:
   x = x.rstrip('\r\n')
   parts = x.split(':')
   hwparts = parts[2].split(',')  # may be hw,L; or just hw
   hw = hwparts[0]
   d[hw]=True
 print len(d.keys()),"keys read from",filein
 return d

def make_prep1keys(filein,fileout,nochangekeys):
 f = codecs.open(filein,encoding='utf-8',mode='r')
 fout = codecs.open(fileout,encoding='utf-8',mode='w')
 nkeep=0
 ndrop=0
 for line in f:  
  # skd-only format.  normkey:key:SKD
  line = line.rstrip('\r\n')
  try:
   (normkey,key,code) = line.split(':')
  except:
   print "PROBLEM.line=",line.encode('utf-8')
   exit(1)
  if key in nochangekeys:
   ndrop=ndrop+1
  else:
   nkeep = nkeep+1
   fout.write('%s\n'%key)
 f.close()
 fout.close()
 print ndrop,"keys dropped from",filein
 print nkeep,"keys from",filein,"written to",fileout

if __name__ == "__main__":
 filein=sys.argv[1] # skd-only
 #filein1=sys.argv[2] # skdnochange
 fileout =sys.argv[2] #  prep1keys

 #nochangekeys = init_nochangekeys(filein1) # a dictionary
 nochangekeys = {}
 make_prep1keys(filein,fileout,nochangekeys)
