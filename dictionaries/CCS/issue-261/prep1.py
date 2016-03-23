# -*- coding: utf-8 -*-
"""prep1.py for ccs
  Mar 21, 2016
 python prep1.py ccs prep1keys.txt ../../../orig/ccs.txt ../../ccshw2.txt prep1.txt prep1.org
"""
import re
import sys,codecs
import transcoder
transcoder.transcoder_set_dir("");

def as2slp1(x):
 y = re.sub(r'-','',x)
 z = transcoder.transcoder_processString(y,'as','slp1')
 return z

def adjust_datalines(dictcode,datalines):
 if dictcode == 'ccs':
  # ccs has one word per line, usually. fabricate new datalines.
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
  # Remove '|', which is a line-separator in CCS
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
  if (icase == 100) and False:  # dbg
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

if __name__ == "__main__":
 dictcode = sys.argv[1].lower()  # dictionary code
 filehw = sys.argv[2] # list of headwords, 1 per line
 filein=sys.argv[3] #  X.txt
 filein1=sys.argv[4] # Xhw2.txt
 fileout1 =sys.argv[5] #  Emacs Org Mode listing
 fileout2 = sys.argv[6] # Markdown listing
 # slurp filehw into list of headwords. These are the ones to check
 with codecs.open(filehw,encoding='utf-8',mode='r') as f:
  headwords  = [x.rstrip('\r\n') for x in f]

 # slurp X.txt file into list of lines
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  inlines = [x.rstrip('\r\n') for x in f]
 # construct headword records
 hwrecs=init_headwords(filein1)
 main(dictcode,headwords,inlines,hwrecs,fileout1,fileout2)
