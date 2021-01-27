""" remove_comma.py
 python remove_comma.py <FILEIN> 
"""
import sys,re,codecs

def main(lines):
 ans = [] # new list of lines
 for line in  lines:
  L,key,wordin = line.split(':')
  words = wordin.split(',')
  for w in words:
   newline = "%s:%s:%s" %(L,key,w)
   ans.append(newline)
 return ans

if __name__ == "__main__":
 filein = sys.argv[1]
 if len(sys.argv) > 2:
  fileout = sys.argv[2]
 else:
  fileout = filein
 with codecs.open(filein,"r","utf-8") as f:
  lines = [x.rstrip('\r\n') for x in f]
  print(len(lines),"read from",filein)
 newlines = main(lines)
 with codecs.open(fileout,"w","utf-8") as f:
  for line in newlines:
   f.write(line + '\n')
 print(len(newlines),"written to",fileout)
 
