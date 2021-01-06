# -*- coding: utf-8 -*-
""" abnormending.py

Usage - python3 abnormending.py lettersAtEnd threshold
e.g. python3 abnormending.py 3 10

This will generate words having 3-letter endings occurring in less than 10 headwords.
"""
from __future__ import print_function
import sys
import codecs
import os
import datetime
from collections import defaultdict
from collections import OrderedDict


# Function to return timestamp
def timestamp():
    return datetime.datetime.now()


def triming(lst):
    output = []
    for member in lst:
        member = member.strip()
        output.append(member)
    return output


def abnormending(n):
    fout = codecs.open('abnorm_' + str(n) + '.txt', 'w', 'utf-8')
    filein = os.path.join('..', '..', 'hwnorm1', 'sanhw1', 'sanhw1.txt')
    fin = codecs.open(filein, 'r', 'utf-8')
    data = fin.readlines()
    data = triming(data)
    res = defaultdict(list)
    for datum in data:
        [word, dict] = datum.split(':')
        end = word[-int(n):]
        res[end].append(datum)
    res1 = OrderedDict(sorted(res.items(), key=lambda t: t[0]))
    for (key, value) in res1.items():
        if len(value) < 10:
            for val in value:
                # Only one dictionary has that thing
                if ',' not in val:
                    print(key, val)
                    fout.write(val + '\n')
    fout.close()


if __name__ == "__main__":
    n = sys.argv[1]
    abnormending(n)
