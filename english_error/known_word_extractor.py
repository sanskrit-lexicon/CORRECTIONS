import os
import codecs
from collections import Counter


dictsWithEnglish = [
    'md', 'wil', 'yat', 'gst', 'ben', 'mw72', 'ap90', 'cae',
    'mw', 'shs', 'mwe', 'bor', 'ae', 'inm', 'vei', 'pui', 'bhs', 'acc', 'ieg',
    'snp', 'pe', 'pgn', 'mci'
]


def find_known_words(code, threshold=1):
    filein = os.path.join('output', code + '_error.txt')
    fileout = os.path.join('knownwords', code + '_knownwords.txt')
    words = []
    fin = codecs.open(filein, 'r', 'utf-8')
    fout = codecs.open(fileout, 'w', 'utf-8')
    for line in fin:
        line = line.rstrip()
        splits = line.split(':')
        errorwords = splits[2]
        words += errorwords.split(',')
    cnt = Counter(words)
    result = []
    for (a, b) in cnt.most_common():
        if b > threshold:
            print(a, '\t', b)
            result.append(a)
    result = sorted(result)
    fout.write('\n'.join(result))
    fin.close()
    fout.close()


if __name__ == "__main__":
    for code in dictsWithEnglish:
        print(code)
        find_known_words(code, 1)
