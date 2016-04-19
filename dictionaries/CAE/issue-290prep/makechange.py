"""makechange.py  Apr 4, 2016
  extract the 'change' records out of prep1_edit.org
  python makechange.py prep1_edit.org change-289.txt
1092 records written to change-261.txt
p 42
t 970
n 80

"""
import sys, re
import codecs
import collections

def update_counts(line,c):
 parts = line.split(':')
 if len(parts) not in [5,6]:
  print "BAD # of parts",line
  exit(1)
 if len(parts) == 5:
  ckey =  parts[3]
 else:
  ckey =  parts[4]
 # check for error conditions
 # if code (ckey) is 'n', then
 # a)  len(parts) should be 5
 # b) and  parts[1] should equal parts[2]
 if ckey == 'n':
  if len(parts) == 6:
   print "PROBLEM at",line.encode('utf-8')
   return
  keyparts = parts[1].split(',')
  key = keyparts[0]
  if key != parts[2]:
   print "PROBLEM at",line.encode('utf-8')
   return  
 c.update([ckey])

def extract(filein,fileout):
 f = codecs.open(filein,'r','utf-8')
 fout = codecs.open(fileout,'w','utf-8')
 # Do some counting as a side benefit of the program
 c = collections.Counter()

 ncaseprev=-1
 nchgprev=0
 nchangetot = 0
 for line in f:
  line = line.rstrip('\r\n')
  m = re.search(r'^[*] TODOx .*? Case (....):',line)
  if m:
   ncase = int(m.group(1))
   if (ncaseprev != -1):
    if nchgprev == 0:
     print "WARNING: No changes for case",ncaseprev
   nchgprev = 0
   ncaseprev = ncase
   continue
  if line.startswith('*'):  # a date comment
   continue
  if line.startswith(';'):
   continue
  if line.strip() == '': # also skip blank lines
   continue
  # assume a change record
  nchgprev = nchgprev + 1
  nchangetot = nchangetot + 1
  update_counts(line,c)
  fout.write('%s\n' % line)
 f.close()
 fout.close()
 print nchangetot,"records written to",fileout
 for key,value in c.iteritems():
  print key,value

if __name__=="__main__":
 filein = sys.argv[1] 
 fileout = sys.argv[2]
 extract(filein,fileout)
