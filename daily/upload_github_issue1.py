""" python upload_github_issue1.py  ejf 21 April 2025
    Adapted from app/correction_response/upload_github_issue.py 
     Dr. Dhaval Patel
     19 October 2019
"""
from __future__ import print_function
import re
import sys
import os
import codecs
import requests
import json

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 print(len(lines),"read from",filein)
 return lines

def read_pending_entries(tsvfile, lastcfrline):
    lst = int(codecs.open(lastcfrline, 'r', 'utf-8').read())
    print('lst=',lst)
    counter = 0
    result = []
    pending_lines = [] # the lines and counter values corresponding to result
    #f = codecs.open(tsvfile, 'r', 'utf-8',errors="ignore")
    #f = codecs.open(tsvfile, 'r', 'utf-8')
    f = open(tsvfile, mode='r', encoding='utf-8')
    try:      
     for iline,line in enumerate(f):
        #print('iline=',iline)
        entry = line.rstrip().split('\t')
        if counter < lst:
            pass
        elif not ':' in entry[-1]:
            #print('case : not in entry[-1]',len(entry))
            print(entry[0])
            date = entry[0]
            dictionary = entry[1].lower()
            lnum = entry[2].lstrip().rstrip()
            headword = entry[3]
            old = entry[4]
            new = entry[5]
            comment = entry[6]
            #print('comment=',comment)
            bodytxt = 'date:\t' + date + '\n' + 'dict:\t' + dictionary + '\n' + 'Lnum:\t'+ lnum + '\n' + 'hw:\t'+ headword + '\n' + 'old:\t' + old + '\n' + 'new:\t' + new + '\n' + 'comm:\t' + comment
            title=dictionary + ':' + lnum
            #print('bodytxt computed')
            #result.append({'body': bodytxt,'title':title})
            result.append({'body': bodytxt,'title':title,'date':date})
            #print('result computed')
            pending_line = (counter,line)
            #print('pendline_line computed')
            pending_lines.append(pending_line)
            #print(pending_line) # dbg
        else:
         print('counter=',counter)
        counter += 1
    except Exception as e:
     print('read_pending_entries error: iline=',iline)
     print("exception=",e)
     print('error at entry date=',date)
     print('len(entry) = ',len(entry))
     #print('line=',line)
     #print('entry=',entry)
     exit(1)
        
    #print('ending counter=',counter)
    #codecs.open(lastcfrline, 'w', 'utf-8').write(str(counter))  #Do this in create_issue
    return pending_lines,result


def prev_create_issue(entry):
    username = os.environ['GITHUB_USER']
    #password = os.environ['GITHUB_PASSWORD']
    token = os.environ['GITHUB_ACCESS_TOKEN']
    #print(username,password)
    #print('entry=',entry)
    s = requests.Session()
    #s.auth = (username, password)
    s.auth = (username, token)
    r = s.post('https://api.github.com/repos/sanskrit-lexicon/csl-orig/issues', json.dumps(entry))
    #print('status code returns:',r.status_code)
    #if r.status_code == requests.codes.created:
    #    print(r.text)
    return r.status_code

def create_issue(entry):
    username = os.environ['GITHUB_USER']
    token = os.environ['GITHUB_ACCESS_TOKEN']
    s = requests.Session()
    s.auth = (username, token)
    urlbase = 'https://api.github.com/repos/sanskrit-lexicon/csl-orig'
    #urlbase = 'https://api.github.com/repos/funderburkjim/testing'

    url = '%s/issues' % urlbase
    r = s.post(url, json.dumps(entry))
    print('status code = ',r.status_code)
    if r.status_code == requests.codes.created:
        print('uploaded issue %s to \n%s' %(entry['title'],url))
    else:
        print('problem uploading issue %s to \n%s' %(entry['title'],url))
    return r.status_code

def upload_cfr(filein):
    with codecs.open(filein,encoding='utf-8',mode='r') as f:
        bodytxt = f.read()
    result = []
    title = filein
    bodytxt1 = "```\n%s\n```" % bodytxt
    entry = {'body': bodytxt1, 'title':title}
    create_issue(entry)
    
if __name__ == "__main__":
    filein = 'cfr_20250419.txt'
    upload_cfr(filein)
    
 
 
