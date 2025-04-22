# coding=utf-8

import sys, re
import urllib.request
from datetime import datetime
import cfr_adj1
import upload_github_issue1

import sys, re,codecs

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 print(len(lines),"read from",filein)
 return lines

def write_lines(fileout,outarr,printFlag=False):
 with codecs.open(fileout,"w","utf-8") as f:
  for out in outarr:
   f.write(out+'\n')
 if printFlag:
  print(len(outarr),"lines written to",fileout)


def check_ymd(date_str):
 try:
  datetime.strptime(date_str, '%Y%m%d')
  return True
 except ValueError:
  return False

cologne_dicts = ('acc', 'ae', 'ap', 'ap90', 'ben', 'bhs', 'bop', 'bor', 'bur', 'cae', 'ccs', 'gra', 'gst', 'ieg', 'inm', 'krm', 'lan', 'lrv', 'mci', 'md', 'mw', 'mw72', 'mwe', 'pd', 'pe', 'pgn', 'pui', 'pw', 'pwg', 'sch', 'shs', 'skd', 'stc', 'vcp', 'vei', 'wil', 'yat')


def partition(lines):
 good = []
 bad = []
 for line in lines:
  parts = line.split('\t')
  d = parts[1]
  if d.lower().strip() in cologne_dicts:
   good.append(d)
  else:
   bad.append(d)
 return good,bad

if __name__== "__main__":
 ymd = sys.argv[1] # yyyymmdd
 cur_ymd = datetime.now().strftime('%Y%m%d')
 if not check_ymd(ymd):
  print('Invalid date. Expect date in format yyyymmdd')
  exit(1)
 if ymd >= cur_ymd:
  print('Date should be < ',cur_ymd)
  exit(1)
 urlfile = 'cfr-%s.tsv' % ymd
 print('Downloading %s' % urlfile)
 urlbase = 'https://www.sanskrit-lexicon.uni-koeln.de/scans/csl-corrections/app/correction_response'
 url = '%s/%s' % (urlbase,urlfile)

 lines = []
 try:
  with urllib.request.urlopen(url) as response:
   for line in response:
    assert type(line) == bytes
    line1 = str(line,'utf-8') # convert to utf-str. type(line1) = str
    line1 = line1.rstrip('\r\n')
    lines.append(line1)
 except:
  print('Error downloading', url)
  exit(1)
  
 nlines = len(lines)
 print(nlines,"lines read from server ",urlfile)
 tsvfilename = urlfile 
 write_lines(tsvfilename,lines,printFlag=True)

 # cfr_...txt  easier to read.
 fileout = 'cfr_%s.txt' %ymd
 cfr_adj1.adjust(tsvfilename,fileout)

 upload_github_issue1.upload_cfr(fileout)

