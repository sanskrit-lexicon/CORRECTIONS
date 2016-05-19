"""hw0_iast.py  ejf  May 9, 2015
 Read the modified pdhw0.txt, compare the SLP1 and IAST forms of each headword,
 and write out differences.  Ignore the 'NOAS' cases.
 May 9, 2015  
"""
import re
import sys,codecs
import transcoder
transcoder.transcoder_set_dir("");

def as2slp1(x):
 y = re.sub(r'-','',x)
 z = transcoder.transcoder_processString(y,'as','slp1')
 return z
def unused_as2slp1_systematic(x):
 y = re.sub(r'-','',x)
 # nasals
 y = re.sub(r'n3([kg])',r'm3\1',y)
 y = re.sub(r'n5([cj])',r'm3\1',y)
 y = re.sub(r'm([pbm])',r'm3\1',y)
 y = re.sub(r'n([tdn])',r'm3\1',y)
 # visarga
 y = re.sub(r'ss','h2s',y)
 # alternate vant/vat  or mant/mat
 y = re.sub(r'va\(n$','vat',y)
 y = re.sub(r'ma\(n$','mat',y)

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

filein=sys.argv[1] # 
fileout =sys.argv[2] #  
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
