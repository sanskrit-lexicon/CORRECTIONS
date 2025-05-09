"""sanhw2.py
 Nov 2, 2015
 A variant. Show the first L-number 
 Oct 26, 2014
 Construct merge of all Cologne Sanskrit-Lexicon dictionaries 
   with Sanskrit headwords.
 Merge the raw headwords into one list.
 The output file contains two fields, separated by colon
  hw  =  the headword spelled in SLP1
  dicts = the Cologne dictionary codes having this hw; separated by 'comma'.
 NO spelling normalization is done, though this may be useful in future
 revisions.
 The output is sorted into Sanskrit alphabetical order by headword.
 Nov 28, 2014  Modified to place M+consonant in the order of 
     [homorganic nasal of consonant]+consonant.
     e.g., aMka  would be (for purpose of ordering) thought of as aNka.
     This is when the consonant is among the 5 vargas.  For other consonants
     (  yrlvSzsh), the ordering remains as M.
 Dec 29, 2014. Revised to make the sort faster.
     Checked it gives same result as prior version.
 Apr 13, 2015. Added specialized dictionaries
 Oct 20, 2016.  Use revised key2 format.
   Currently, SKD has extra fields  (see skd/2012/pywork/make_xml.py)
   This program is changed to parse both this (new) format, and the
   old formats
"""
import sys,re
import codecs

# dictyear has all dictionary codes, with the 'year'.
# This 'year' is required to locate the files
# This is a Python dictionary data structure, quite like a PHP associative array
dictyear={"ACC":"2014" , "AE":"2014" , "AP":"2014" , "AP90":"2014",
       "BEN":"2014" , "BHS":"2014" , "BOP":"2014" , "BOR":"2014",
       "BUR":"2013" , "CAE":"2014" , "CCS":"2014" , "GRA":"2014",
       "GST":"2014" , "IEG":"2014" , "INM":"2013" , "KRM":"2014",
       "MCI":"2014" , "MD":"2014" , "MW":"2014" , "MW72":"2014",
       "MWE":"2013" , "PD":"2014" , "PE":"2014" , "PGN":"2014",
       "PUI":"2014" , "PWG":"2013" , "PW":"2014" , "SCH":"2014",
       "SHS":"2014" , "SKD":"2013" , "SNP":"2014" , "STC":"2013",
       "VCP":"2013" , "VEI":"2014" , "WIL":"2014" , "YAT":"2014"}
# sandicts is list of dictionaries with Sanskrit Headwords
# only the 'general' dictionaries are included.
san_en_dicts = ["WIL","YAT","GST","BEN","MW72","AP90","CAE","MD",
               "MW","SHS","BHS","AP","PD"]
san_fr_dicts = ["BUR","STC"]
san_de_dicts = ["PWG","GRA","PW","CCS","SCH"]
san_lat_dicts = ["BOP"]
san_san_dicts = ["SKD","VCP"]
san_spc_dicts = ["INM","VEI","PUI","ACC","KRM","IEG","SNP","PE","PGN","MCI"]
sandicts = san_en_dicts + san_fr_dicts + san_de_dicts + san_lat_dicts +san_san_dicts + san_spc_dicts

def extracthw_mw(filein):
 try: 
  f = codecs.open(filein,"r","utf-8")
 except:
  print "ERROR extracthw_mw file not found:",filein
  exit(1)
 hws = []
 for line in f:
  line = line.rstrip('\r\n')
  (hw,dummy1,dummy2) = re.split('\t',line)
  recs = re.split(r';',dummy2)
  firstrec = recs[0]
  (hcode,L1,L2) = re.split(r',',firstrec)
  L = L1  # use first L
  hws.append((hw,L))
 f.close()
 return hws

def old_extracthw(filein):
 try: 
  f = codecs.open(filein,"r","utf-8")
 except:
  print "ERROR extracthw file not found:",filein
  exit(1)
 hws = []
 L = 0
 for line in f:
  line = line.rstrip('\r\n')
  (dummy,hw,dummy) = re.split(':',line)
  L = L + 1
  hws.append((hw,L))
 f.close()
 return hws

class HW2(object):
 def __init__(self,line,n):
  line = line.strip() # remove starting or ending whitespace
  self.line = line
  self.n = n
  parts = re.split(':',line)
  if len(parts) == 5:
   (self.pagecol,self.hw,self.line12,self.L,self.type) = parts
  elif len(parts) == 4:
   (self.pagecol,self.hw,self.line12,self.L) = parts
   self.type='n' # default 'normal'
  elif len(parts) == 3:
   (self.pagecol,self.hw,self.line12) = parts
   self.L = n  # default, line number within hw2 file
   self.type='n'

def init_hw2(filein):
 recs=[]
 with open(filein,'r') as f:
  n = 0
  for line in f:
   n = n + 1
   rec = HW2(line,n)
   recs.append(rec)
 #print len(recs),"records from",filein
 return recs

def extracthw(filein):
 recs = init_hw2(filein)
 hws = [(rec.hw,rec.L) for rec in recs]
 return hws

def addhw(code,d):
 """ Uses global dictyear to locate codehw2.txt file 
 """
 try:
  year = dictyear[code]
 except:
  print "ERROR dictyear has no code",code
  exit(1)
 # dirmain example:  PWGScan/2013/  if code == PWG
 dirmain = "%sScan/%s/" %(code,year)
 # "../../"  due to relative location of this program file
 # Nov 2, 2015.  the 'hws' variable now contains a list of strings,
 # each string having the form 'hw;L', where 'L' is the L-number of the
 # first record containing the given 'hw'.  
 dirbase = dirin = "../../" + dirmain
 if code == 'MW': 
  filein = dirbase + "mwaux/mwkeys/extract_keys_b.txt"
  hws = extracthw_mw(filein)
 else:
  # hw2name = pwghw2.txt  for code = PWG
  hw2name = "%shw2.txt" % code.lower()
  filein = dirbase + "pywork/" + hw2name
  hws = extracthw(filein)
 print "%s hws extracted from dict %s" %(len(hws),filein)
 # add these to 'd'
 for (hw0,L) in hws:
  # hw0 is a unicode string. Convert.
  hw = hw0.encode('ascii','replace')
  curval = '%s;%s' %(code,L)  # semi
  if not hw in d:
   d[hw] = [curval]
  else:
   oldvals = d[hw]
   found=False
   for val in oldvals:
    (code1,L1) = re.split(r';',val)
    if code == code1:
     found=True
   if not found:
    d[hw].append(curval)

import string
# Note 'L' and '|' and 'Z' and 'V' are not present
# Not sure where they go
tranfrom="aAiIuUfFxXeEoOMHkKgGNcCjJYwWqQRtTdDnpPbBmyrlvSzsh"
tranto = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvw"
trantable = string.maketrans(tranfrom,tranto)

def slp_cmp_pairs(a,b):
 return slp_cmp(a[1],b[1]) # normalized

def slp_cmp(a,b):
 a1 = string.translate(a,trantable)
 b1 = string.translate(b,trantable)
 return cmp(a1,b1)

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
def slp_cmp1_helper(a):
 a = re.sub(r'(M)([kKgGNcCjJYwWqQRtTdDnpPbBm])',slp_cmp1_helper1,a)
 return a
def slp_cmp1(a,b):
 a = slp_cmp1_helper(a)
 b = slp_cmp1_helper(b)
 a1 = string.translate(a,trantable)
 b1 = string.translate(b,trantable)
 return cmp(a1,b1)

def sanhw1(fileout):
 # d is a dictionary
 # key is headword
 # value is list of dict codes
 d = {}
 test = False
 if test:
  dicts = ["MW","PW"] # for testing
  print "Testing with dicts=",dicts
 else:
  print "Using all",len(sandicts),"dictionaries"
  dicts = sandicts
 for code in dicts:
  addhw(code,d)
 # sort hws
 hws = d.keys()
 opt=2 # controls which way
 if opt==1:
  # previous way
  sortedhws = sorted(hws,cmp=slp_cmp1)
 else:
  # new way
  hwpairs = [(hw,slp_cmp1_helper(hw)) for hw in hws]
  sorted_hwpairs = sorted(hwpairs,cmp=slp_cmp_pairs)
  sortedhws = [hw for (hw,hwadj) in sorted_hwpairs]
 # output 
 fout = codecs.open(fileout,"w","utf-8")
 for hw in sortedhws:
  codes = sorted(d[hw])
  codestr = ','.join(codes)
  fout.write("%s:%s\n"%(hw,codestr))
 fout.close()
 print "%s hws written to %s" %(len(hws),fileout)
if __name__=="__main__":
 fileout = sys.argv[1] # output path
 sanhw1(fileout)

