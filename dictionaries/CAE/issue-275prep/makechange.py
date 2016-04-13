""" makechange.py  Apr. 12, 2015
   python makechange.py alphaerr_edit.txt alphaerr_change.txt alphaerr_other.txt
"""
import sys,re,codecs
import collections

class Input(object):
 def __init__(self,parts,L,line):
  self.line = line
  self.L = L
  self.page = parts[0]
  self.key1 = parts[1]
  self.line12 = parts[2]
  if parts[3]!= 'X':
   print "X expected ERROR at line",L
   print line.encode('utf-8')
   return
  self.keynew = parts[4]
  self.errcode = parts[5]
  self.comment = parts[6]

def init_input(filein,fileout1):
 f = codecs.open(filein,"r","utf-8")
 fout1 =codecs.open(fileout1,"w","utf-8")
 nout1=0
 count1 = collections.Counter()
 recs=[]
 n = 0
 for line in f:
  n = n+1
  L = n # imputed L-number
  line = line.rstrip('\r\n')
  m = re.search(r'^([0-9])+:([^:])+:([^:])+:$',line)
  if m:
   # this is a standard line of input, which can be ignored
   continue
  parts = line.split(':')
  nparts = len(parts)
  # two cases. A change 'X', or some comment
  if nparts not in [7,4]:
   print "Problem at line",n
   print "line=",line.encode('utf-8')
   continue
  if nparts == 4:
   # just print out to the alternate output file
   fout1.write("%s\n" % line)
   nout1=nout1+1
   # update counter 
   code = parts[3][0]
   count1.update(code)
   continue
  rec = Input(parts,L,line)
  recs.append(rec)
 f.close()
 fout1.close()
 print n,"records processed from",filein
 print nout1,"records written to",fileout1
 print len(recs),"change records parsed"
 for code in count1.keys():
  print code,count1[code]
 return recs
def main(filein,fileout,fileout1):
 recs = init_input(filein,fileout1)
 dictcode = 'cae'
 with codecs.open(fileout,"w","utf-8") as f:
  for rec in recs:
   keyL = "%s,%d" %(rec.key1,rec.L)
   out = ':'.join( [dictcode,keyL,rec.keynew,rec.errcode,rec.comment])
   f.write('%s\n' % out)
 print len(recs),"lines written to",fileout

if __name__=="__main__":
 filein = sys.argv[1]
 fileout = sys.argv[2]
 fileout1 = sys.argv[3]
 main(filein,fileout,fileout1)
