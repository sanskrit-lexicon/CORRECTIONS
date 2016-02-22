"""possibledisp1.py  Feb 22, 2016
 python possibledisp1.py pui_possible_plurals.txt possibledisp1.txt
"""
import re
#import transcoder
import sys,codecs
import requests
class Possible(object):
 def __init__(self,line):
  line=line.strip()
  self.line=line
  try:
   parts=re.split(r':',line)
   if len(parts) == 2:
    self.key1=parts[0]
    dictstr=parts[1]
   else:
    self.key1=parts[1]
    dictstr=parts[2]
   self.dicts = re.split(r',',dictstr)
  except:
   print "PROBLEM with line:",line.encode('utf-8')
   exit(1)

def init_possible(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs=[Possible(x) for x in f]
 return recs

def escape(x):
 return x

def disp1_textify(rec,s,icase):
 """ 
 """
 #regex = re.compile('<table>(.*?)</table>',flags=re.DOTALL)
 #print s.encode('utf-8')
 #print "---------------------------------------"
 tables = re.findall('<table.*?>(.*?)</table>',s,flags=re.DOTALL)
 outarr=[]
 #outarr.append("%s TABLES found" % len(tables)) # always 1
 outarr.append("-"*60)
 outarr.append("Case %03d: %s" %(icase,rec.line))
 for table in tables:
  rows = re.findall('<tr.*?>(.*?)</tr>',table,flags=re.DOTALL)
  # outarr.append("TABLE has %s rows"%len(rows)) may be more than 1 row
  for row in rows:
   cols = re.findall('<td.*?>(.*?)</td>',row,flags=re.DOTALL)
   #outarr.append(" ROW has %s columns:"%len(cols)) always 1 column
   for col in cols:
    col = re.sub(r'<br/?>','\n',col)
    lines = re.split('\n',col)
    for line in lines:
     line = re.sub(r'&nbsp;',' ',line)
     line = re.sub('<.*?>','',line)
     line = line.strip()
     outarr.append("  %s" % line)
     
 out = '\n'.join(outarr)   
 return out

def disp1(rec,icase):
 urlbase="http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/getword.php"
 key = rec.key1
 output = 'slp1'
 inputx='slp1'
 dictcode='PUI'
 accent='no'
 payload={'key':key,'output':output,'input':inputx,'accent':accent,'dict':dictcode}
 r = requests.get(urlbase,params=payload)
 if r.status_code == requests.codes.ok:
  out = disp1_textify(rec,r.text,icase)
 else:
  out = "Status code for %s is %s" %(key,r.status_code)
 return out

if __name__ == "__main__":
 filein=sys.argv[1] 
 fileout =sys.argv[2] 
 possibles=init_possible(filein)
 recs = possibles #[0:5]
 fout = codecs.open(fileout,'w','utf-8')
 icase=0
 for rec in recs:
  icase = icase+1
  out = disp1(rec,icase)
  fout.write("%s\n" %out)
 fout.close()

