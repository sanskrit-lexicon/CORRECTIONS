"""hw0.py  ejf  2014-06-25
 Read digitization pd.txt.
 Output all major headwords, along with the page on which the headword appear.
 Also, output the line numbers in pd.txt that pertain to the headword.
 - Page numbers are like [Page1-001b+ 54] (This is the first, appearing on l.55)
   [PageV-XC+ N]
   V is a 1-digit volume number (1 to 8)
   X is a 3- or 4-digit-sequence (the page number (cumulative)), and 
   C is the column (a or b)
   N is number of following lines in this column.
 - Note: starting with volume 7, Page numbers are coded slightly diffferently!
   [PageV-X-C+ N]  (an extra '-' before the column number
 - Headwords are as in headword.py
   X is coded in HK encoding 
   It is checked that 'X' contains no colon character.
 - line numbers l1,l2 are the first line number and last line number of 
   pd.txt that pertain to the headword.  
 -  There is no 'extra' material at the end.
 - There is one 'extra' line at the beginning
 The output is written as  (note: 'page' is V-X)
  page:headword:line1,line2
 May 9, 2015  
"""
import re
import sys,codecs
filename=sys.argv[1] # 
fileout =sys.argv[2] #  
f = codecs.open(filename,encoding='utf-8',mode='r')
fout = codecs.open(fileout,'w','utf-8')

n = 0
nb = 0 # number of left brackets
nout = 0 # number of headword lines written to output
rePage = re.compile(r"\[Page(.*?)]")
import headword
reHeadword0 = headword.reHeadword
reHeadword = re.compile(reHeadword0)
l0=0 # first line number for a headword
nhw=0 # same as n, but stops when the 'end' string is found
#first line of file, not processed (NOTE: IS PROCESSED FOR VEI)
firststring=r'%***This'
firstfound=False
endstring=r'XXXXXXXXXX'  #not really needed. file is read to end
endfound=False
isFirst = False
page  = "1-0001a"
# collect the output lines into an array.
# Adjust this array (null operation for PD!), 
# and then output the adjusted array
outlines = []
for line in f:
 n = n+1
 line = line.rstrip()
 if (line.find(endstring) >= 0): 
  print "found endstring at n = %s" % n
  endfound=True
 nhw = nhw + 1
 if (line.find(firststring) >= 0) and (not firstfound):
  firstfound=True
  # If  True, DO process this line (to get line number)
  isFirst = False
  print "found firststring"
  continue
 # the placement of m=.. before if(not firstfound) is important detail
 m = reHeadword.search(line)
 reHeadword1 = headword.reHeadword + r" \((.*?)\)"  # May 9, 2015
 m1 = re.search(reHeadword1,line)
 if (not firstfound):
  out = "skip line %s: %s" %(n,line)
  print out.encode('utf-8')
  continue
 if m and (not isFirst):
  # found next headword
  if (l0 != 0):
   # output the prior word
   l1 = l0
   l2 = nhw - 1
   out = "%s:%s:%s,%s:%s" %(page0,hw0,l1,l2,hw0as)
   outlines.append(out)
   nout = nout + 1
  # the base headword. This program outputs this
  hw0 = m.group(1) 
  if m1:
   hw0as = m1.group(3)
  else:
   hw0as = "NOAS"
  # update page0,  l0 
  page0 = page
  l0=nhw
  if re.search(":",hw0):
   out = "Removing from ':' to end at line %s: %s" % (n,hw0)
   print out.encode('utf-8')
   nb = nb + 1
   hw0 = re.sub(':.*$','',hw0)
 # step 3, search for page
 isFirst = False # required for first word handling
 pages = rePage.findall(line)
 if len(pages) > 0:
  pagelast = pages[-1]
  m = re.match(r'^([1-8])-([0-9]+)-?([ab])',pagelast)
  if m:
   volume = m.group(1)
   pagenum = m.group(2)
   if (len(pagenum)==3):
    pagenum = '0' + pagenum # prepend 0
   if (len(pagenum)!=4):
    print "ERROR: Unexpected page number: %s" % m.group(2)
    exit(1)
   page = "%s-%s%s" % (m.group(1),pagenum,m.group(3))
 if endfound:
  break
# we must now prepare the last headword
l1 = l0
l2 = nhw
out = "%s:%s:%s,%s:%s" %(page0,hw0,l1,l2,hw0as)
outlines.append(out)
nout = nout + 1
#---------Adjust outlines.  This logic is skipped for pd

# remove non-dictionary end-of-volume lines
outlines1 = []
for i in xrange(0,nout):
 j = i + 1
 outlines1.append(outlines[i])

#---------Output adjusted lines
nout = 0
for out in outlines1:
 fout.write("%s\n" %(out,))
 nout = nout + 1
f.close();
fout.close();
print "file %s has %s lines" % (filename,n)
print "%s headwords written to file %s" % (nout,fileout)
print "%s headwords contained a colon" % (nb,)
