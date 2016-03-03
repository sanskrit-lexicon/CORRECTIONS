"""foreignwords.py  for IEG
  Mar 2, 2016
 python foreignwords.py ../../../orig/ieg.txt ../../ieghw2.txt foreignwords.txt foreignwords.org
"""
import re
import sys,codecs
import transcoder
transcoder.transcoder_set_dir("");

def as2slp1(x):
 y = re.sub(r'-','',x)
 z = transcoder.transcoder_processString(y,'as','slp1')
 return z

def foreignword(datalines):
 """ Search for various strings in the text, and return a list of
     those strings that match
 """
 searchstrings = [
  ('Tamil','Tamil'),
  ('Telugu-Kannad2a','Telugu-Kannada'),
  ('Telugu','Telugu'),
  ('Telugu-Sanskrit','Telugu-Sanskrit'),
  ('Kannad2a','Kannada'),
  ('Sanskrit-Kannad2a','Sanskrit-Kannada'),
  ('Persian','Persian'),
  ('Prakrit','Prakrit'),
  ('Greek','Greek'),
  ('<P>{%rupee,%}','English'), # one special case
 ]
 found=[]
 #searchlines = datalines # Too many false positives
 searchlines = [datalines[0]]  # just search first line
 for (s,sp) in searchstrings:
  s1 = s.lower()
  for x in searchlines:
   if x.lower().find(s1) != -1:
    if sp not in found:
     found.append(sp)
 return sorted(found)

def main(inlines,hwrecs,fileout,fileout1):
 fout=codecs.open(fileout,"w","utf-8")
 fout1=codecs.open(fileout1,"w","utf-8")
 nsystematic=0
 nout=0
 for hwrec in hwrecs:
  datalines = inlines[hwrec.linenum1-1:hwrec.linenum2]
  # is it a foreign word? If so, get list of languages.
  fw = foreignword(datalines) 
  if len(fw) == 0:
   continue
  firstline = datalines[0] 
  page0 = hwrec.pagecol
  l1 = hwrec.linenum1
  l2 = hwrec.linenum2
  hw0 = hwrec.hwslp
  nout = nout + 1
  dictcode='ieg'
  # output to fileout
  out = "%s:%s:foreign %s" %(dictcode,hw0,','.join(fw))
  fout.write("%s\n" % out)
  # output to fileout1
  outarr=[]
  baseurl='http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=%s'% dictcode
  url = '%s&page=%s' %(baseurl,page0)
  pageref = "[[%s][page %s]]" %(url,page0)
  outarr.append('* TODO Case %04d: %s %s' % (nout, hw0,pageref))
   # output up to 10 lines of datalines
  outlines = datalines[0:10]
  for x in outlines:
   y = transcoder.transcoder_processString(x,'as','roman')
   outarr.append(';  %s' % y)
  if len(datalines)>10:
   ndiff = len(datalines) - 10
   outarr.append(';   [and %s more lines]' % ndiff)
  # 1 extra blank line
  outarr.append('')
  fout1.write('\n'.join(outarr) + "\n")
  if (nout == 25) and False:
   print "debug",nout
   break
   pass
 fout.close()
 fout1.close()
 print len(hwrecs),"headword records processed"
 print nout,"records written to ",fileout
 print nout,"sections written to ",fileout1

 
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
 filein=sys.argv[1] #  X.txt
 filein1=sys.argv[2] # Xhw2.txt
 fileout =sys.argv[3] #  
 fileout1 =sys.argv[4] #  Emacs Ord Mode listing
 # slurp X.txt file into list of lines
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  inlines = [x.rstrip('\r\n') for x in f]
 # construct headword records
 hwrecs=init_headwords(filein1)
 main(inlines,hwrecs,fileout,fileout1)
