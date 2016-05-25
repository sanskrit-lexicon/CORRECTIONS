""" preverb1_change.py
    Generate part of standard changes for the records from preverb1.txt that
    were identified as problems. (These are in file preverb1_prob.txt)

    python preverb1_change.py preverb1_prob.txt preverb1_change.txt
"""
import codecs,re,sys

class Analysis(object):
 def __init__(self,line,option):
  line = line.rstrip('\r\n')
  self.line = line
  parts = re.split('\t',line)
  nparts=len(parts)
  if (option == 'init') and (nparts == 5):
   pass
  elif (option != 'init') and (nparts == 8):
   pass
  else:
   print "Analysis ERROR. %s and %s inconsistent" %(option,nparts)
   print "line=",line.encode('utf-8')
   exit(1)
  (self.H,self.L,self.key1,self.key2,self.lex) = parts[0:5]
  # use self.lex to get self.type (type of record)
  m = re.search(r'^(m|f|n|ind|LEXID|INFLECTID|LOAN|NONE|VERB|ICF|SEE)',self.lex)
  if not m:
   print "Analysis. UNEXPECTED lex:",self.lex.encode('utf-8')
   print "  line=",line.encode('utf-8')
   exit(1)
  code=m.group(1)
  if code in ('m','f','n','ind'):
   self.type='S' # normal Substantive or indeclineable 
  elif code in ('LEXID','INFLECTID','LOAN'):
   self.type='S1' # special substantive
  else:
   self.type=code
  if nparts == 5:  # form of all.txt
   self.analysis='' 
   self.note='init'
   if self.type in ('S','S1'):
    self.status = 'TODO'
   else:
    self.status = 'NTD' # Nothing To Do
  elif nparts == 8:
   (self.analysis,self.status,self.note) = parts[5:]
  else:
   print "Analysis, INTERNAL ERROR:",nparts
   print "Should be either 5 or 8 tab-delimited parts"
   print "line=",line.encode('utf-8')
   exit(1)
  self.parent = None  # determined by init_parents. 
  self.parenta = None # determined by init_parentsa.

 def __repr__(self):
  note=self.note
  if self.status == 'TODO':
   if self.parent:
    note = '%s:parent=%s'%(self.note,self.parent.key1)
    if self.parent.type == 'VERB':
     note = "%s:VERB"%note
  parts=(self.H,self.L,self.key1,self.key2,self.lex,self.analysis,self.status,note) 
  return '\t'.join(parts)

def main(recs):
 recs1 = []
 nrecs = len(recs)
 for irec in xrange(0,nrecs):
  rec = recs[irec]
  if rec.lex != 'VERB:K':  # prefixed verb
   continue
  if rec.H not in ['1','2']:
   continue
  # look for a sequence of '3' and/or '4' records following
  jrec = irec + 1
  jrec1 = irec
  jrec2 = 0
  #while (jrec < nrecs) and (recs[jrec].H in ['3','4']):
  while (jrec < nrecs) and (recs[jrec].H.startswith(('3','4'))):
   jrec2 = jrec
   jrec = jrec+1
  if jrec2 == 0:
   continue
  # found our case
  recs1.append(recs[jrec1])
  for jrec in xrange(jrec1+1,jrec2+1):
   # write only the '3' cases
   if recs[jrec].H == '3':
    recs1.append(recs[jrec]) 
 return recs1
def init_analysis(filein,option):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Analysis(x,option) for x in f]
 print len(recs),"records read from",filein
 return recs

if __name__ == "__main__":
 filein  = sys.argv[1] # 
 fileout = sys.argv[2]
 #recs = init_analysis(filein,'init')
 #recs1 = main(recs)
 f = codecs.open(filein,"r","utf-8")
 fout = codecs.open(fileout,"w","utf-8")
 code=None
 for line in f:
  line = line.rstrip('\r\n')
  m = re.search(r'^; *err=(.*?)$',line)
  if m:
   code = m.group(1)
   fout.write(line + '\n')
   continue
  if line.startswith(';'): # comment
   fout.write(line + '\n')
   continue
  rec = Analysis(line,'init')
  lastfield = rec.lex
  (lex,data) = re.split(r' *[*]+ *',lastfield)
  if code == 'key1':
   newkey2 = data
   newkey1 = re.sub(r'[~-]','',newkey2)
   out = 'mw:%s,%s:%s:t: key1 error'%(rec.key1,rec.L,newkey1)
  elif code == 'key2':
   newkey2 = data
   out = 'mw:%s,%s:%s:%s:t: key2 error'%(rec.key1,rec.L,rec.key2,newkey2)
  elif code == 'H':
   oldH = rec.H # does not have the initial 'H'
   newH = data  # has the initial 'H'
   out = 'mw:%s,%s:H%s>:%s>:t: H-code error'%(rec.key1,rec.L,oldH,newH)
  else:
   print "ERROR CODE problem",code
   exit(1)
  fout.write('%s\n' % out)
 fout.close()

  
