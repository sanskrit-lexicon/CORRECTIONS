import re
import codecs

regex = r'\(([A-Z][^.]*)[.]\)'
filein = '/var/www/html/cologne/wil/orig/wil.txt'
fin = codecs.open(filein, 'r', 'utf-8')
data = fin.read()
entries = data.split('<LEND>')
for entry in entries:
    match = re.search(regex, entry)
    if match:
        print(match.group(1))
