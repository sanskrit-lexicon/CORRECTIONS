""" alphaerr_prep1.py
 For CAE.  List all of hw2.txt, with a mark to indicate those that
 are out of alphabetical order.
 python alphaerr_prep1.py ../../caehw2.txt alphaerr_prep1.txt
"""
import sys, re
import codecs

import string
tranfrom="aAiIuUfFxXeEoOMHkKgGNcCjJYwWqQRtTdDnpPbBmyrlvSzsh"
tranto = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvw"
trantable = string.maketrans(tranfrom,tranto)
def slp_cmp(a,b):
 a1 = string.translate(a,trantable)
 b1 = string.translate(b,trantable)
 return cmp(a1,b1)

class Vrec(object):
 def __init__(self,line,page,colline,n):
  self.line = line # the text
  self.page = page # the page (a string)
  self.col =  ''  # No column. The col within page (a string)
  self.colline = colline # the line number within the column of the page.
  self.n = n # integer line number within file (starting at 1)

def alphaerr_lineP(x):
 if '{??}' in x:
  return True
 return False


class Hwrec(object):
 def __init__(self,line,n):
  line = line.rstrip('\r\n')
  self.line = line # the text
  self.n = n # integer line number within file (starting at 1)
  (self.pageref,self.hwslp,self.linenum12) = re.split(r':',line)
  
  # next required for use in slp_cmp
  (self.linenum1,self.linenum2) = re.split('[,]',self.linenum12)
  self.digitization = None # to be filled later

def init_hwrecs(filein):
 #f = codecs.open(filein,encoding='utf-8',mode='r')
 # filein is ascii file (vcphw2.txt)
 # read it as Ascii so slp_cmp string.translate works
 f = codecs.open(filein,mode='r') 
 recs = [] 
 n = 0 # count of lines in file
 for line in f:
  n = n + 1
  recs.append(Hwrec(line,n))
 f.close()
 return recs

def make_txt(hwrecs,fileout,ifirst=0,ilast=999999):
 fout = codecs.open(fileout,'w','utf-8') 
 # read headword lines, and generate output
 n = 0 # count of lines read
 lnum = 0 # generate record number for xml records constructed
 icase = 0
 caselist=[]
 for i in xrange(1,len(hwrecs)):
  rec1 = hwrecs[i-1]
  rec2 = hwrecs[i]
  hw1 = rec1.hwslp
  hw2 = rec2.hwslp
  if slp_cmp(hw1,hw2) <= 0:
   status=''
  else:
   status='X'
   icase = icase + 1
  fout.write('%s:%s\n' %(rec1.line,status))
 # write last line
 status=''
 fout.write('%s:%s\n' %(rec2.line,status))
 # close output
 fout.close()
 # informational message
 print icase,"headwords found out of order. Search with ':X'"

if __name__=="__main__":
 
 filein = sys.argv[1]  # Xhw2.txt
 fileout = sys.argv[2]
 # slurp hw2.txt  into Hwrec objects
 hwrecs = init_hwrecs(filein)
 make_txt(hwrecs,fileout)
 exit(1)
 # slurp vcp.txt into array of lines
 vrecs = []
 with codecs.open(filein,'r','utf-8') as f:
  vrecs=[line.rstrip('\r\n') for line in f]
 # put the first line in vrecs into hwrec records
 for hwrec in hwrecs:
  n1 = int(hwrec.linenum1) - 1
  line = vrecs[n1]
  hwrec.digitization = line
 make_txt(hwrecs,fileout,ifirst,ilast)

