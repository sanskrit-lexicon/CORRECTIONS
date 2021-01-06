# -*- coding: utf-8 -*-
""" abnormending.py

Usage - python3 abnormending.py lettersAtEnd
e.g. python3 abnormending.py 3

To generate words ending with abnormal endings (maybe less than 50 headwords).
"""
from __future__ import print_function
import sys
import re
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
        if len(value) < 50:
            for val in value:
                # Only one dictionary has that thing
                if ',' not in val:
                    print(key, val)
                    fout.write(val + '\n')
    exit(0)
    """
    for (end, datum) in output:
        if end not in endings:
            endings.append(end)
            print(end)
    print(len(endings))
    withcounter = []
    for ends in endings:
        counter = 0
        for datum in data:
            if re.search(ends + ':', datum):
                counter += 1
        if counter < 50:
            withcounter.append((counter, ends))
            print(counter, ends)
        else:
            print(ends + 'has more than 50 words')
    withcounter = sorted(withcounter, key=lambda x: x[0])
    print("Culled out and sorted abnormal endings")

    print("Writing suspect entries to abnorm.txt.")
    print("This would take some time.")
    nochange = codecs.open('../nochange/nochange1.txt', 'r', 'utf-8')
    noc = nochange.readlines()
    noc = triming(noc)
    for (count, end) in withcounter:
        for datum in data:
            if re.search(end + ':[^,]*$', datum) and datum not in noc:
                fout.write(datum + "\n")
    fout.close()
    """

if __name__ == "__main__":
    n = sys.argv[1]
    abnormending(n)
