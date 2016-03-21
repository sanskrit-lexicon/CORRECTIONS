# -*- coding: utf-8 -*-
"""verbs1.py for BHS
  Mar 2, 2016
 python verbs1.py ../../../orig/bhs.txt ../../bhshw2.txt verbs1.txt verbs1.org
"""
import re
import sys,codecs
import transcoder
transcoder.transcoder_set_dir("");

def as2slp1(x):
 y = re.sub(r'-','',x)
 z = transcoder.transcoder_processString(y,'as','slp1')
 return z

def verb1(datalines,hw):
 """ Search for various strings in the text, and return a list of
     those strings that match
 """
 
 searchstrings = [  # regex
  (u' n[.] of ','noun','data'), # do this first
  (u'ati$','Verb 3s P','hw'), # for search in hw
  (u'ate$','Verb 3s A','hw'), # for search in hw

 ]
 found=[]
 #searchlines = datalines # Too many false positives
 searchlines = [datalines[0]]  # just search first line
 for (s,sp,code) in searchstrings:
  s1 = s
  found1=False
  if code == 'data':
   searchlinesuse = searchlines
  else:
   searchlinesuse = [hw]
  for x in searchlinesuse:
   #x = re.sub(r' etc[.]','',x)
   if re.search(s1,x):
    found.append(sp)
    found1=True # so outer loop also breaks
    break  # just one classification
  if found1:
   break
 return sorted(found)

nonverbs=['ajitAvati','aDipati','anantabalaviGuzwaninAditaSrIsaMBavamati',
'anihitamati','aruRavati','Agatigati','AguhyakADipati','Arati',
'unnati','ojopati','kaccati','kumudAkaramati','KamBIrapati',
'gajapati','gaRanAgati','gati','gatikA','guhyakADipati',
'guhyADipati','gfhapati','Gozamati','jagamantrasAgaranirGozamati',
'diSAMpati','durgati','dvayamati','DarmaDAtvarcivErocanasaMBavamati','Darmamati',
'DarmAkaramati','niyati','nirati','nirmARarati','paYcASati',
'padmAkaramati','paryAdinna','prajApati','prativirati','praBaketurAjamati',
'pravarAgramati','Badramati','mahAgati','mahADipati','lokapati',
'varAgramati','vasumati','viBUtapati','vimati','vImati',
'vyAvADa','SarIragati','Sezapati','SrIpraBAsamati','saMgati',
'saMtati', 'saBApati','samati','sahaMpati','sahApati',
'sImAvati','surati','sUmati','prapati','sahAMpati',
]

dverbs={}  # {'hve':'Verb Misc',

def disp_org(icase,wordtype,hw0,url,page0,datalines):
 """ return array of lines, formatted for details of Emacs org mode
 """
 outarr=[]
 pageref = "[[%s][page %s]]" %(url,page0)
 outarr.append('* Case %04d: %s %s %s ' % (icase, wordtype,hw0,pageref))
  # output up to 10 lines of datalines
 outlines = datalines[0:10]
 for x in outlines:
  # Remove '|', which is a line-separator in BHS
  x = re.sub(r'[|]','',x)
  y = transcoder.transcoder_processString(x,'as','roman')
  outarr.append(';  %s' % y)
 if len(datalines)>10:
  ndiff = len(datalines) - 10
  outarr.append(';   [and %s more lines]' % ndiff)
 outarr.append('')
 return outarr

def disp_md(icase,wordtype,hw0,url,page0,datalines):
 """ return array of lines, formatted for details of GitHub Markdown
 """
 outarr=[]
 pageref = "[page %s](%s)" %(page0,url)
 outarr.append(' Case %04d: %s **%s** %s ' % (icase, wordtype,hw0,pageref))
  # output up to 10 lines of datalines
 outlines = datalines[0:10]
 outarr.append('```')
 for x in outlines:
  # Remove '|', which is a line-separator in BHS
  x = re.sub(r'[|]','',x)
  y = transcoder.transcoder_processString(x,'as','roman')
  if (y.strip() != ''):
   outarr.append('%s' % y)
 if len(datalines)>10:
  ndiff = len(datalines) - 10
  outarr.append('  [and %s more lines]' % ndiff)
 outarr.append('```')
 outarr.append('------------------------------------------')
 outarr.append('')
 return outarr

def main(inlines,hwrecs,fileout,fileout1,fileouta,fileout1a,fileout2,fileout2a):
 fout=codecs.open(fileout,"w","utf-8")
 fout1=codecs.open(fileout1,"w","utf-8")
 fouta=codecs.open(fileouta,"w","utf-8")
 fout1a=codecs.open(fileout1a,"w","utf-8")
 fout2=codecs.open(fileout2,"w","utf-8")
 fout2a=codecs.open(fileout2a,"w","utf-8")
 nsystematic=0
 nout=0
 nouta=0
 for hwrec in hwrecs:
  datalines = inlines[hwrec.linenum1-1:hwrec.linenum2]
  # is it a foreign word? If so, get list of languages.
  hw0 = hwrec.hwslp
  if hw0 in nonverbs:
   continue
  L = hwrec.lnum
  fw = verb1(datalines,hw0) 
  if len(fw) == 0:  # len(fw) is always 1
   continue
  wordtype=fw[0] # in this case, len(fw) = 1
  # skip some
  if not wordtype.startswith('Verb'):
   continue
  # for dev, just print the Verb? cases
  #if not wordtype.startswith('Verb?'):
  # continue
  firstline = datalines[0] 
  page0 = hwrec.pagecol
  l1 = hwrec.linenum1
  l2 = hwrec.linenum2
  # decide which output this case goes to
  # (a) a 'simple root' or
  # (b) a 'verb form'
  # decide this on basis of 'hw0'
  # In almost all cases, (a) occurs when there is only one vowel in hw0.
  m = re.findall(r'[aAiIuUfFxXeEoO]',hw0)
  if False: #(len(m) == 1) or (hw0=='UrRu'):
   (wordtype,f,f1,f2) = ('Root',fout,fout1,fout2)
   nout = nout+1
   icase = nout
  else:
   (wordtype,f,f1,f2) = ('Verb form',fouta,fout1a,fout2a)
   nouta = nouta + 1
   icase = nouta
  dictcode='bhs'
  # output to fileout
  #out = "%s:%s: %s" %(dictcode,hw0,','.join(fw))
  out = "%s:%s,%s: %s" %(dictcode,hw0,L,wordtype)
  f.write("%s\n" % out)
  # output to Org mode and Markdown
  baseurl='http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=%s'% dictcode
  url = '%s&page=%s' %(baseurl,page0)
  # org mode
  outarr = disp_org(icase,wordtype,hw0,url,page0,datalines)
  f1.write('\n'.join(outarr))
  # markdown
  outarr = disp_md(icase,wordtype,hw0,url,page0,datalines)
  f2.write('\n'.join(outarr))
  if ((nout+nouta) == 100) and False:  # dbg
   print "debug",icase
   break
   pass
 fout.close()
 fout1.close()
 fouta.close()
 fout1a.close()
 print len(hwrecs),"headword records processed"
 print nout,"records written to ",fileout
 print nout,"sections written to ",fileout1
 print nouta,"records written to ",fileouta
 print nouta,"sections written to ",fileout1a

 
class Headword(object):
 def __init__(self,line,n):
  line = line.rstrip('\r\n')
  self.line = line
  self.lnum = n
  (self.pagecol,self.hwslp,linenum12) = re.split('[:]',line)
  (linenum1,linenum2) = re.split(r',',linenum12)
  self.linenum1=int(linenum1)
  self.linenum2=int(linenum2)

def init_headwords(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  recs = []
  lnum=0
  for x in f:
   lnum = lnum+1
   recs.append(Headword(x,lnum))
 return recs

if __name__ == "__main__":
 filein=sys.argv[1] #  X.txt
 filein1=sys.argv[2] # Xhw2.txt
 fileout =sys.argv[3] #  
 fileout1 =sys.argv[4] #  Emacs Org Mode listing
 fileouta =sys.argv[5] #  
 fileout1a =sys.argv[6] #  Emacs Org Mode listing
 fileout2 = sys.argv[7] # Markdown listing
 fileout2a = sys.argv[8] # Markdown listing

 # slurp X.txt file into list of lines
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  inlines = [x.rstrip('\r\n') for x in f]
 # construct headword records
 hwrecs=init_headwords(filein1)
 main(inlines,hwrecs,fileout,fileout1,fileouta,fileout1a,fileout2,fileout2a)
