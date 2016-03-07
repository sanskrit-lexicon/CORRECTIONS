
import re,codecs,sys
if __name__ == "__main__":
 filein=sys.argv[1]
 fileout = sys.argv[2]
 verbs = []
 nonverbs=[]
 with codecs.open(filein,"r","utf-8") as f:
  for x in f:
   x = x.rstrip('\r\n')
   if not x.startswith('* '):
    continue
   m = re.search(r'^[*] ([^ ]+) TODO Case .....: Verb[?] (.*?) ',x)
   if not m:
    continue
   code = m.group(1)
   hw = m.group(2)
   code = code.strip()
   if code == 'x':
    nonverbs.append("'" + hw + "'")
    continue
   if code.lower() == 'm':
    code='Misc'
   elif re.search(r'^[1-9]',code):
    code = "class %s" % code
   dverb = " '" + hw + "':'Verb " +code + "',"
   verbs.append(dverb)
 with codecs.open(fileout,"w","utf-8") as fout:
  for i in xrange(0,len(nonverbs),5):
   out = ' , '.join(nonverbs[i:i+5])
   fout.write(' %s ,\n' % out)
  fout.write('\n\n')
  for dverb in verbs:
   fout.write('%s\n' % dverb)
 fout.close()
