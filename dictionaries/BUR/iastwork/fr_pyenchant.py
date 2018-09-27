# coding=utf-8
""" fr_pyenchant.py
 python fr_pyenchant <input> <french> <outputok> <outputprob>
 <input> = filename of 'extracted' file.
 <french> = code name of French dictionary = fr_FR

 Requires virtualenv with enchant installed. See readme.org.
    
    
"""
import sys,re,codecs
import enchant

def check(filein,dictname,fileoutok,fileoutprob):
 try:
  french = enchant.Dict(dictname)
 except:
  print "ERROR. Bad dictionary name:",dictname
  exit(1)

 n=0
 foutok = codecs.open(fileoutok,'w','utf-8')
 foutprob = codecs.open(fileoutprob,'w','utf-8')
 f =  codecs.open(filein,encoding='utf-8',mode='r')
 nok = 0
 nprob = 0
 nerr = 0
 for line in f:
  line = line.rstrip('\r\n')
  n=n+1
  (word,count)=re.split(r' +',line)
  try:
   ok = french.check(word)
  except:
   out = "enchant error 1: line=%s" % line
   print out.encode('utf-8')
   nerr=nerr+1
   continue
  if ok:
   nok = nok + 1
   foutok.write("%s\n" % line)
   continue
  # remove ending period, dash
  # and initial -
  word1 = re.sub(r'[.-]+$','',word)
  word1 = re.sub(r'^[-]+','',word1)
  try:
   ok = french.check(word1)
  except:
   out = "enchant error 2: line=%s" % line
   print out.encode('utf-8')
   nerr=nerr+1
   continue
  if ok:
   nok = nok + 1
   foutok.write("%s\n" % line)
   continue
  # no luck
  nprob = nprob + 1
  foutprob.write("%s\n" % line)
 f.close()
 foutok.close()
 foutprob.close()

 print "%s records read from %s" %(n,filein)
 print "%s words written to %s" %(nok,fileoutok)
 print "%s words written to %s" %(nprob,fileoutprob)
 print "%s enchant errors" %nerr

if __name__=="__main__":
 filein = sys.argv[1] # extract
 dictname = sys.argv[2] # fr_FR
 fileoutok = sys.argv[3] # ok
 fileoutprob = sys.argv[4] # prob
 check(filein,dictname,fileoutok,fileoutprob)
