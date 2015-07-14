""" checkHxa.py  Jul 12, 2015
 Read a version of monier.xml, and check that key1 for each HxA is the
 same as for the parent.  This prompted by a user-discovered counterexample.
 Usage: python checkHxa.py monier.xml checkHxa.txt log_20150712-01.txt
 Usage2: After corrections, downloaded new temp/monier.xml
 python checkHxa.py temp/monier.xml temp/checkHxa.txt temp/log_20150714-01.txt
"""
import sys, re,codecs

class Counter(dict):
 def __init__(self):
  self.d = {}
 def update(self,l):
  for x in l:
   if not (x in self.d):
    self.d[x]=0
   self.d[x] = self.d[x] + 1


def checkHxa(filein,fileout,fileupd):
 fout = codecs.open(fileout,"w",'utf-8')
 f = codecs.open(filein,"r",'utf-8')
 fupd = codecs.open(fileupd,"w",'utf-8')
 n = 0 # number of lines read
 nprob = 0 # Number of lines changed
 chgCounter = Counter() # categories changed
 for line in f:
  line = line.rstrip('\r\n')
  m = re.search(r'<(H[^>]*)>.*?<key1>(.*?)</key1>.*?<key2>(.*?)</key2>.*<L[^>]*>(.*?)</L>',line)
  if not m:
   #fout.write(line)
   continue
  n = n + 1
  cat = m.group(1)
  keyH = m.group(2)
  key2 = m.group(3)
  L=m.group(4)
  if re.search(r'[1-4]$',cat):
   parent = keyH
   parent2 = key2
  elif cat.endswith('A') and (keyH !=parent):
   nprob = nprob + 1
   out = "-"*72
   fout.write("%s\n" % out)
   out = "case %03d: %s %s != %s" %(nprob,L,keyH,parent)
   fout.write("%s\n" % out)
   fout.write("old:\n%s\n" %line)
   new = line
   new = re.sub(r'<key1>.*?</key1>','<key1>%s</key1>'%parent,new)
   new = re.sub(r'<key2>.*?</key2>','<key2>%s</key2>'%parent2,new)
   fout.write("new:\n%s\n" %new)
   # write update record to 'log' file
   fupd.write("Update\n")
   fupd.write("<L>%s</L>\n" % L)
   fupd.write("%s\n" % new)
  continue
 fout.close()
 f.close()
 print n,"lines from",filein
 print nprob,"lines to",fileout
if __name__=="__main__": 
 filein = sys.argv[1] #  monier.xml
 fileout = sys.argv[2] # checkHxa.txt
 fileupd = sys.argv[3] # log....txt
 checkHxa(filein,fileout,fileupd)
