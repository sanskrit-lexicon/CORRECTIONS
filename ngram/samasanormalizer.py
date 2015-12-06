# -*- coding: utf-8 -*-
"""
python samasanormalizer.py inputfile outputfile

"""
import sys, re
import codecs
import string
import datetime
import itertools

# Function to return timestamp
def timestamp():
	return datetime.datetime.now()
def unique(lst):
	output = []
	for member in lst:
		if member not in output:
			output.append(member)
	return output

# Asked the procedure at http://stackoverflow.com/questions/34108900/optionally-replacing-a-substring-python
lstrep = [('A',('A','aa','aA','Aa','AA')),('I',('I','ii','iI','Ii','II')),('U',('u','uu','uU','Uu','UU')),('F',('F','ff','fx','xf','Fx','xF','FF')),('e',('e','ea','ai','aI','Ai','AI')),('o',('o','oa','au','aU','Au','AU','aH','aHa')),('E',('E','ae','Ae','aE','AE')),('O',('O','ao','Ao','aO','AO'))]	
global solutions
solutions = {}
def permut(word,lstrep,dictionary):
	input_str = word

	# make substitution list a dict for easy lookup
	lstrep_map = dict(lstrep)
	# a substitution is an index plus a string to substitute. build
	# list of subs [[(index1, sub1), (index1, sub2)], ...] for all
	# characters in lstrep_map.
	subs = []
	for i, c in enumerate(input_str):
		if c in lstrep_map:
			subs.append([(i, sub) for sub in lstrep_map[c]])
	# build output by applying each sub recorded
	out = []
	for sub in itertools.product(*subs):
		# make input a list for easy substitution
		input_list = list(input_str)
		for i, cc in sub:
			if ''.join(input_list[:i])+cc[0] in dictionary:
				input_list[i] = cc
		out.append(''.join(input_list))
	out = unique(out)
	return out
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

dictionary = []
with open('../../hwnorm1/normalization/hw1.txt') as f:
	for line in f:
		line = line.strip()
		if len(line) > 2:
			dictionary.append(line)
inputword = 'rAmAyaReSvaraputrapratipatti'
if len(inputword) < 125:
	inputwords = permut(inputword,lstrep,dictionary)
	print inputwords
	for word in inputwords:
		print word
		splits = find_words(word,dictionary)
		if splits is not None:
			print splits
			break
else:
	print find_words(inputword,dictionary)
"""
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
"""
