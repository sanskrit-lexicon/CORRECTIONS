# sample_detect.py.  written for Python 3
import codecs, sys, re
from google.cloud import translate
import languagecodes

# Instantiates a client
translate_client = translate.Client()

class Rec(object):
 def __init__(self,line):
  line = line.rstrip('\r\n')
  try:
   (self.word,self.countstr) = line.split(' ')
  except:
   print('ERROR in',line)
   exit(1)
  self.language = 'None'
  self.confidence = 0.0

def init_burtexts(filein):
 recs = []
 with codecs.open(filein,'r','utf-8') as f:
  recs = [Rec(x) for x in f if not x.startswith(';')]
 print(len(recs),'records read from',filein)
 return recs

def init_languagecodes():
 languages = languagecodes.languages  # a list of 2-tuples
 d = {}
 for code,langname in languages:
  # for ease of later parsing, replace space with _
  langname = langname.replace(' ','_')
  d[code] = langname
 return d

def detect(recs):
 langdict = init_languagecodes()
 texts = [rec.word for rec in recs]
 results = translate_client.detect_language(texts)
 for iresult,result in enumerate(results):
  rec = recs[iresult]
  rec.language = result['language']
  rec.confidence = result['confidence']
  if rec.language in langdict:
   rec.langname = langdict[rec.language]
  else:
   rec.langname = rec.language + '?'

if __name__ == "__main__":
 filein = sys.argv[1]
 fileout = sys.argv[2]
 recs = init_burtexts(filein)
 detect(recs) # modify recs
 with codecs.open(fileout,'w','utf-8') as f:
  for rec in recs:
   out = '%s %s %s %.2f' %(rec.word, rec.countstr,rec.langname,rec.confidence)
   f.write(out + '\n')
 print(len(recs),"results written to",fileout)

