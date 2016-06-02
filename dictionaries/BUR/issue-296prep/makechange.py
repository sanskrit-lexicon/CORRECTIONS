"""makechange.py  June 2, 2016
  extract the 'change' records out of hwchk_iast1.org
  python makechange.py hwchk_iast1_edit.org change_296prep.txt


"""
import sys, re
import codecs
import collections

def update_counts(line,c,caseid):
 parts = line.split(':')
 if len(parts) not in [5,6]:
  print "BAD # of parts",line
  exit(1)
 if len(parts) == 5:
  ckey = 'DEVA' + '-' + parts[3]
 else:
  ckey = 'IAST' + '-' + parts[4]
 c.update([ckey])
 if ckey.endswith('n'):
  #print "WARNING: 'n' change code for case",caseid
  if ckey =='DEVA-n':
   print "WARNING: %s: Case %s: %s" %(ckey,caseid,line)
class Case(object):
 def __init__(self,caseid,caselines):
  self.id = caseid
  self.lines = caselines
  # check that it is marked
  self.devachg = None
  self.iastchg = None
  self.change = None
  if not self.lines[1].startswith(';'):
   self.devachg = self.lines[1]
   self.change=self.devachg
  if not self.lines[2].startswith(';'):
   self.iastchg = self.lines[2]
   self.change=self.iastchg
  if (self.iastchg != None) and (self.devachg != None):
   print caseid,"WARNING: both IAST and DEVA are changed"
  if (self.iastchg == None) and (self.devachg == None):
   print caseid,"WARNING: no changes"

def init_records(filein):
 cases=[]  # list of Case records returned
 f = codecs.open(filein,'r','utf-8')
 caselines=[]
 for line in f:
  line=line.rstrip()
  m = re.search(r'^[*] TODOx Case ([0-9]+):',line)
  if not m:
   if len(caselines)==0:
    continue # skip any lines previous to first case
   else:
    # append line to current caselines
    caselines.append(line)
    continue
  # new case, output prior case, if present
  if len(caselines)>0:
   case = Case(caseid,caselines)
   cases.append(case)
  # generate new case
  caseid = m.group(1)
  caselines=[line]
 # generate last case
 case = Case(caseid,caselines)
 cases.append(case)
 f.close()
 print len(cases),"cases initialized"
 #exit(1) # for debug
 return cases

def extract(filein,fileout):
 fout = codecs.open(fileout,'w','utf-8')
 # Do some counting as a side benefit of the program
 c = collections.Counter()
 cases = init_records(filein)
 ncaseprev=-1
 nchgprev=0
 nchangetot = 0
 for case in cases:
  ncase = int(case.id)
  if (case.iastchg == None) and (case.devachg == None):
   print "skipping case",case.id,case.lines[0].encode('utf-8')
   continue
  nchgprev = nchgprev + 1
  nchangetot = nchangetot + 1
  line = case.change
  update_counts(line,c,case.id)
  fout.write('%s\n' % line)
 fout.close()
 print nchangetot,"records written to",fileout
 for key,value in c.iteritems():
  print key,value

if __name__=="__main__":
 filein = sys.argv[1] 
 fileout = sys.argv[2]
 extract(filein,fileout)
