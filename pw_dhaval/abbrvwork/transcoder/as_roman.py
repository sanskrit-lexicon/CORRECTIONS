"""convert.py
  Python example of transcoding
"""
import sys,codecs,re,string
#sys.path.append('../')
import transcoder
#transcoder.transcoder_set_dir('.');

def convert(filein,fileout,tranin,tranout):
 fp = codecs.open(filein,"r",'utf-8')
 fpout = codecs.open(fileout,"w",'utf-8')
 n=0;
 for b in fp:
  exp = b.split("@")
  x = exp[0]
  exp[4] = exp[4].strip()
  x = x.rstrip('\r\n')
  y = x.lower()
  y = y[0].upper()+y[1:]
  if (y == ''):
   continue
  n=n+1
  z = transcoder.transcoder_processString(y,tranin,tranout)
  fpout.write("%s@%s@%s@%s@%s@%s\n" % (z,exp[0],exp[1],exp[2],exp[3],exp[4]))
 fp.close()
 fpout.close()
 print n,"lines converted to IAST and stored in abbrvoutput/sortedcrefsiast.txt\n"
#-----------------------------------------------------
if __name__=="__main__":
 filein = sys.argv[1]
 fileout = sys.argv[2]
 tranin = sys.argv[3]
 tranout = sys.argv[4]
 convert(filein,fileout,tranin,tranout)
