"""hwchk_iast1.py  ejf  for benfey
  Apr 21, 2016  Modified to make use of hwnorm1c
  Apr 20, 2016
  python hwchk_iast1.py ../../../orig/ben.txt ../../benhw2.txt hwchk_iast1.txt hwchk_iast1.org  <path to hwnorm1c.txt>
  Modified from similar program for PD
May 9, 2015
 Read the modified pdhw0.txt, compare the SLP1 and IAST forms of each headword,
 and write out differences.  Ignore the 'NOAS' cases.
 May 9, 2015  
"""
import re
import sys,codecs
import transcoder
transcoder.transcoder_set_dir("");
import headword
reHeadword0 = headword.reHeadword
reHeadword = re.compile(reHeadword0)
reHeadword1 = headword.reHeadword + r" *\{%(.*?)%}" 

def as2slp1(x):
 y = re.sub(r'[ +.;-]','',x)
 y = re.sub(r',+$','',y)
 y = re.sub(r'\(\?\)','',y)
 y = re.sub(r'\(=.*?\)','',y)
 y = re.sub(r'\(.*?\)$','',y)
 y = re.sub(r'=.*$','',y)  # represent variant
 y = re.sub(r',.*$','',y)
 y = y.lower()  # BENFEY represents IAST of verbs in capital letters
 z = transcoder.transcoder_processString(y,'as','slp1')
 return z

slp1_cmp1_helper_data = {
 'k':'N','K':'N','g':'N','G':'N','N':'N',
 'c':'Y','C':'Y','j':'Y','J':'Y','Y':'Y',
 'w':'R','W':'R','q':'R','Q':'R','R':'R',
 't':'n','T':'n','d':'n','D':'n','n':'n',
 'p':'m','P':'m','b':'m','B':'m','m':'m'
}
def slp_cmp1_helper1(m):
 #n = m.group(1) # always M
 c = m.group(2)
 nasal = slp1_cmp1_helper_data[c]
 return (nasal+c)

def normalize_key(a):
 #1. normalize so that M is used rather than homorganic nasal
 a = re.sub(r'(M)([kKgGNcCjJYwWqQRtTdDnpPbBm])',slp_cmp1_helper1,a)
 #2. normalize so that 'rxx' is 'rx' (similarly, fxx is fx)
 a = re.sub(r'([rf])(.)\2',r'\1\2',a)
 #3. ending 'aM' is 'a' (Apte)
 a = re.sub(r'aM$','a',a)
 #4. ending 'aH' is 'a' (Apte)
 a = re.sub(r'aH$','a',a)
 #4a. ending 'uH' is 'u' (Apte)
 a = re.sub(r'uH$','u',a)
 #4b. ending 'iH' is 'i' (Apte)
 a = re.sub(r'iH$','i',a)
 #5. 'ttr' is 'tr' (pattra v. patra)
 a = re.sub(r'ttr','tr',a)
 #6. ending 'ant' is 'at'
 a = re.sub(r'ant$','at',a)
 #7. 'cC' is 'C'
 a = re.sub(r'cC','C',a)
 return a

def find_hwnorm1c(hw,dictcode=None):
 """ When dictcode is a dictionary code, then return 
     a 'not found' record when either
     (a) normalized hw is not in hwnorm1c OR
     (b) normlized hw is ONLY in dictionary 'dictcode'
     When dictcode is not a known dictionary code (such as the 
      default value None, then return a 'not found' record when
      (a) occurs.
 """
 hwn = normalize_key(hw)
 notfound = "%s:%s: NOT FOUND" %(hw,hwn)
 if hwn in HWnormc.normd:
  rec = HWnormc.normd[hwn]
  # be sure that word does not occur ONLY in dictcode
  dicts = rec.distinctdicts # a list, upper case
  if dictcode:
   dictcodeu = dictcode.upper()
  else:
   dictcodeu = dictcode
  if dicts != [dictcodeu]:
   return rec.line
  else:
   #  hw occurs only in dictcode 
   return notfound
 # hw not a known word
 return notfound

def check_hwnorm1c(hw,hw1,dictcode):
 return (find_hwnorm1c(hw,dictcode),find_hwnorm1c(hw1,dictcode))
 
def main(inlines,hwrecs,fileout,fileout1):
 dictcode='ben'
 fout=codecs.open(fileout,"w","utf-8")
 fout1=codecs.open(fileout1,"w","utf-8")
 nsystematic=0
 nout=0
 nprob=0
 for hwrec in hwrecs:
  if nprob > 100:
   print "exiting. too many problems"
   break
  datalines = inlines[hwrec.linenum1-1:hwrec.linenum2]
  firstline = datalines[0] 
  m = reHeadword.search(firstline)
  if not m:
   print "UNEXPECTED:",hwrec.line.encode('utf-8')
   continue
  #hw0 = m.group(1)
  # prefer the already normalized hwrec.hwslp
  hw0 = hwrec.hwslp
  m1 = re.search(reHeadword1,firstline)
  if m1:
   hw0as = m1.group(2)
  else:
   hw0as = "NOAS"
   continue  # nothing to do here
  hw1 = as2slp1(hw0as)
  #hw0 = hwrec.hwslp
  if hw1 == hw0:
   continue
  # There are some systematic differences between IAST and Devanagari
  # This is the 'normalization' logic of hwnorm1
  # For Benfey, skip this normalize_key logic, as hw0 already has done it
  #hwnorm = normalize_key(hw0)
  #hw1norm = normalize_key(hw1)
  hwnorm = hw0
  hw1norm = hw1
  if hwnorm == hw1norm:
   nsystematic = nsystematic + 1
   continue
  # Apr 21, 2016. Apply normalize_key to both hwnorm and hw1norm, and
  # note which of the normalized keys is in hwnorm1c.txt
  # see find_hwnorm1c for significance of third parameter (here it is None)
  (hwnormchk,hw1normchk) = check_hwnorm1c(hwnorm,hw1norm,None)
  page0 = hwrec.pagecol
  l1 = hwrec.linenum1
  l2 = hwrec.linenum2
  line = "%s:%s:%d,%d:%s" %(page0,hw0,l1,l2,hw0as)
  if re.search(r'[()*\[]',hw1norm) or re.search(r'[()*\[]',hwnorm):
   out = "BADCHAR: %s:%s" % (line,hw1)
   print out.encode('utf-8')
   print '%d old %s' %(hwrec.linenum1,firstline.encode('utf-8'))
   print 'ben:%s,%d:%s:%s:t:' %(hwrec.hwslp,hwrec.linenum1,'X','Y')
   print
   nprob = nprob+1
   continue
  # difference unresolved
  if re.search('[0-9]',hw1norm):
   out = "NUMCHAR: %s:%s" % (line,hw1)
   print out.encode('utf-8')
   print '%d old %s' %(hwrec.linenum1,firstline.encode('utf-8'))
   print 'ben:%s,%d:%s:%s:t:' %(hwrec.hwslp,hwrec.linenum1,'X','Y')
   print
   nprob = nprob+1
   continue
  nout = nout + 1
  # output to fileout
  out = "%s:%s" %(line,hw1norm)
  fout.write("%s\n" % out)
  # output to fileout1
  outarr=[]
  baseurl='http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=%s'% dictcode
  url = '%s&page=%s' %(baseurl,page0)
  pageref = "[[%s][page %s]]" %(url,page0)
  outarr.append('* TODO Case %04d: %s %s' % (nout, hw0,pageref))
  # construct two possible correction 'change' records
  keyref = "%s,%s" %(hwrec.hwslp,hwrec.lnum)
  out = ':'.join([dictcode,keyref,hw1,'n',''])
  outarr.append(';%s' % out)
  out = ':'.join([dictcode,keyref,hw0as,hw0as,'n',''])
  outarr.append(';%s' % out)
  # Apr 21, 2016. output result of search in hwnorm1c
  outarr.append('; ' +hwnormchk)
  outarr.append('; ' +hw1normchk)

  # output up to 10 lines of datalines
  outlines = datalines[0:10]
  for x in outlines:
   outarr.append(';  %s' % x)
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
 print nsystematic,"systematic IAST/DEVA differences ignored"

 
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

class HWnormc(object):
 normd = {} 
 def __init__(self,line):
  line = line.rstrip('\r\n')
  self.line=line
  m = re.search(r'^(.*?):(.*?)$',line)
  self.hwnorm=m.group(1)
  self.code=None # modified later
  self.explain = None # modified later
  data = m.group(2)
  variants = re.split(r';',data)
  self.keys = []
  self.dicts = []
  self.distinctdicts=[]
  for variant in variants:
   (key,dictstr) = re.split(r':',variant)
   dictlist = re.split(r',',dictstr)
   self.keys.append(key)
   self.dicts.append(dictlist)
   for d in dictlist:
    if d not in self.distinctdicts:
     self.distinctdicts.append(d)
  if self.hwnorm in HWnormc.normd:
   print "HWnormc: unexpected duplicate",self.hwnorm
  HWnormc.normd[self.hwnorm] = self

def init_hwnorm1c(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [HWnormc(line) for line in f]
 print len(recs),"records from",filein
 return recs

if __name__ == "__main__":
 filein=sys.argv[1] #  ben.txt
 filein1=sys.argv[2] # benhw2.txt
 fileout =sys.argv[3] #  
 fileout1 =sys.argv[4] #  Emacs Org Mode listing
 filehwnorm1c = sys.argv[5]
 init_hwnorm1c(filehwnorm1c)
 # slurp ben.txt file into list of lines
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  inlines = [x.rstrip('\r\n') for x in f]
 # construct headword records
 hwrecs=init_headwords(filein1)
 main(inlines,hwrecs,fileout,fileout1)
 exit(1)
 f = codecs.open(filein,encoding='utf-8',mode='r')
 fout = codecs.open(fileout,'w','utf-8')
 n = 0
 nout = 0
 nsystematic = 0
 for line in f:
  n = n+1
  line = line.rstrip()
  (pagecol,hw0,line12,hw0as) = re.split(':',line)
  if hw0as == 'NOAS':
   continue
  hw1 = as2slp1(hw0as)
  if hw1 == hw0:
   continue
  # There are some systematic differences between IAST and Devanagari
  # This is the 'normalization' logic of hwnorm1
  hwnorm = normalize_key(hw0)
  hw1norm = normalize_key(hw1)
  # also, IAST gives alternate ma(n)t and va(n)t.
  # At this point, our logic may have hw1norm as ma(n or va(n
  hw1norm = re.sub(r'a\(n$','at',hw1norm)
  # Also, IAST has 'ss' while slp1 has Hs
  hw1norm = re.sub(r'ss','Hs',hw1norm)
  # Similarly, 'SS' -> 'HS', and zz -> Hz
  hw1norm = re.sub(r'SS','HS',hw1norm)
  hw1norm = re.sub(r'zz','Hz',hw1norm)
 
  if hwnorm == hw1norm:
   nsystematic = nsystematic + 1
   continue
  if re.search(r'[()*\[]',hw1norm) or re.search(r'[()*\[]',hwnorm):
   out = "BADCHAR: %s:%s" % (line,hw1)
   print out.encode('utf-8')
   continue
  # difference unresolved
  nout = nout + 1
  fout.write("%s:%s\n" % (line,hw1norm))
  if re.search('[0-9]',hw1norm):
   out = "NUMCHAR: %s:%s" % (line,hw1)
   print out.encode('utf-8')
   
 f.close()
 fout.close()
 print n,"records read from ",filein
 print nout,"records written to ",fileout
 print nsystematic,"systematic IAST/DEVA differences ignored"
 
