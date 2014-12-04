"""sanhw1.py
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
sandicts = san_en_dicts + san_fr_dicts + san_de_dicts + san_lat_dicts +san_san_dicts

def extracthw_mw(filein):
 try: 
  f = codecs.open(filein,"r","utf-8")
 except:
  print "ERROR extracthw_mw file not found:",filein
  exit(1)
 hws = []
 for line in f:
  line = line.rstrip('\r\n')
  (hw,dummy,dummy) = re.split('\t',line)
  hws.append(hw)
 f.close()
 return hws

def extracthw(filein):
 try: 
  f = codecs.open(filein,"r","utf-8")
 except:
  print "ERROR extracthw file not found:",filein
  exit(1)
 hws = []
 for line in f:
  line = line.rstrip('\r\n')
  (dummy,hw,dummy) = re.split(':',line)
  hws.append(hw)
 f.close()
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
 for hw0 in hws:
  # hw0 is a unicode string. Convert.
  hw = hw0.encode('ascii','replace')
  if not hw in d:
   d[hw] = [code]
  else:
   if code not in d[hw]:
    d[hw].append(code)

import string
# Note 'L' and '|' and 'Z' and 'V' are not present
# Not sure where they go
tranfrom="aAiIuUfFxXeEoOMHkKgGNcCjJYwWqQRtTdDnpPbBmyrlvSzsh"
tranto = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvw"
trantable = string.maketrans(tranfrom,tranto)
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
 dicts = ["MW","PW"] # for testing
 dicts = sandicts
 for code in dicts:
  addhw(code,d)
 # sort hws
 hws = d.keys()
 sortedhws = sorted(hws,cmp=slp_cmp1)
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

