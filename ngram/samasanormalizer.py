# -*- coding: utf-8 -*-
"""
python samasanormalizer.py inputfile outputfile

"""
import sys, re
import codecs
import string
import datetime

# Function to return timestamp
def timestamp():
	return datetime.datetime.now()
# Code of Rems http://stackoverflow.com/questions/8870261/how-to-split-text-without-spaces-into-list-of-words is slightly modified for Sanskrit.
def find_words(instring,dictionary):
    global solutions
    # First check if instring is in the dictionnary
    if instring in dictionary:
        return [instring]
    # No... But maybe it's a result we already computed
    if instring in solutions:
        return solutions[instring]
    # Nope. Try to split the string at all position to recursively search for results
    best_solution = None
    for i in range(1, len(instring) - 1):
        part1 = find_words(instring[:i],dictionary)
        part2 = find_words(instring[i:],dictionary)
        # Both parts MUST have a solution
        if part1 is None or part2 is None:
            continue
        solution = part1 + part2
        # Is the solution found "better" than the previous one?
        if best_solution is None or len(solution) < len(best_solution):
            best_solution = solution
    # Remember (memoize) this solution to avoid having to recompute it
    solutions[instring] = best_solution
    return best_solution


if __name__=="__main__":
    fin = sys.argv[1]
    fout = sys.argv[2]
    words = set()
    h = codecs.open(fout,'w','utf-8')
    global solutions
    solutions = {}
    with open('../../hwnorm1/normalization/hw1.txt') as f:
        for line in f:
            line = line.strip()
            if len(line) > 2:
                words.add(line)
    with open(fin) as g:
        for line in g:
            headword = line.split(':')[2].strip()
            words.discard(headword)
            if find_words(headword,words) is None:
                h.write(line)
    h.close()					
