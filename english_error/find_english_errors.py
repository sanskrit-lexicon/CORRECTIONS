# -*- coding: utf-8 -*-
"""Find potential errors in the English description in Cologne dictionaries.

Author - drdhaval2785@gmail.com
Date - 01 January 2021

Usage - python3 find_english_errors.py
"""
import re
import os
import codecs
import xml.etree.ElementTree as ET
import enchant
from indic_transliteration import sanscript


sanskritTags = {
    'md': ['b', 's', 'i'],
    'wil': ['s', 'i'],
    'yat': ['s', 'i'],
    'gst': ['s', 'i'],
    'ben': ['s', 'i'],
    'mw72': ['s', 'i', 'nsi'],
    'ap90': ['s', 'i'],
    'cae': ['s', 'i', 'ab', 'lang', 'lex'],
    'mw': ['srs', 's', 'i', 'ab', 'lang', 'lex', 'etym', 's1', 'ls', 'bot'],
    'shs': ['s', 'i'],
    'mwe': ['s', 'i'],
    'bor': ['s'],
    'ae': ['s'],
    'inm': ['i'],
    'vei': ['b', 'i'],
    'pui': ['i'],
    'bhs': ['b'],
    'acc': ['s'],
    'ieg': ['i'],
    'snp': ['i', 'bot'],
    'pe': [],
    'pgn': ['i'],
    'mci': ['i', 'b'],
    'lan': ['b', 'i']
}

startIdentifier = {
    'md': r',',
    'wil': r'\)',
    'yat': r'  ',
    'gst': r'  ',
    'ben': r'  ',
    'mw72': r'<',
    'ap90': r'',
    'cae': r'  ',
    'mw': r'  ',
    'shs': r'  ',
    'mwe': r'<i>',
    'bor': r'  ',
    'ae': r'',
    'inm': r'  ',
    'vei': r'  ',
    'pui': r'  ',
    'bhs': r'',
    'acc': r'  ',
    'ieg': r'  ',
    'snp': r'  ',
    'pe': r'  ',
    'pgn': r'  ',
    'mci': r'  ',
    'lan': r'<i>',
}


dictsWithEnglish = [
    'md', 'wil', 'yat', 'gst', 'ben', 'mw72', 'ap90', 'cae',
    'mw', 'shs', 'mwe', 'bor', 'ae', 'inm', 'vei', 'pui', 'bhs', 'acc', 'ieg',
    'snp', 'pe', 'pgn', 'mci', 'lan'
]


def ignore_anglicised_sanskrit(line, identifier):
    if identifier != '':
        line = re.sub('^[^' + identifier + ']*' + identifier, '', line)
    return line


def exclude_tags(line, tagsToExclude):
    # Removal of ls and ab tags for all dictionaries
    for tag in ['ls', 'ab']:
        line = re.sub(r'<' + tag + r'[^>]*>[^<]*</' + tag + '>', r'', line)
    # Removal of tags and contents for tags containing Sanskrit words.
    for tag in tagsToExclude:
        # <s1 slp1="ahicCattra">Ahicchattra</s1>
        line = re.sub(r'<' + tag + r'[^>]*>[^<]*</' + tag + '>', r'', line)
    # Generic removal of remaining tags, without removing its content.
    line = re.sub('<[^<]+>', '', line)
    # continue hyphens
    line = re.sub(r'[\-][ ]+', '-', line)
    return line


def return_ascii_words(line):
    splits = re.split(r'[ ;,\?\.\!\_—]', line)
    words = []
    for split in splits:
        m = re.split(r'[\-]+', split)
        # Remove empty strings.
        # https://stackoverflow.com/questions/3845423/remove-empty-strings-from-a-list-of-strings
        m = list(filter(None, m))
        # If items separated by hyphen are proper words, split them.
        # Otherwise remove the hyphen and join them.
        if len(m) > 1:
            if all(verify_word(a, base_dict) for a in m):
                words += m
        elif re.search('^[\x00-\x7F]+$', split):
            split = re.sub('[^a-zA-Z]', '', split)
            # Ignore blank entries and entries starting with capital letters.
            # See https://github.com/sanskrit-lexicon/csl-corrections/issues/28#issuecomment-753334079
            if split != '' and not re.search('^[A-Z]', split):
                words.append(split)
    return words


def verify_word(word, base_dict):
    # If the word itself is in the base dictionary, return true.
    result = base_dict.check(word)
    # Else,
    if not result:
        # Preprocess the word for common items missing pyenchant library.
        word1 = word.lower()
        # surpassingly->surpassing
        word1 = re.sub('ily$', 'y', word)
        word1 = re.sub('ly$', '', word1)
        # intactness->intact, diseaseless->disease
        word1 = re.sub('iness$', 'y', word1)
        word1 = re.sub('ness$', '', word1)
        word1 = re.sub('iless$', 'y', word1)
        word1 = re.sub('less$', '', word1)
        # unliberal->liberal
        word1 = re.sub('^[uU]n', '', word1)
        # awakener->awaken
        word1 = re.sub('er$', '', word1)
        # instructor->instruct
        word1 = re.sub('ctor$', 'ct', word1)
        # humiliator->humiliate
        word1 = re.sub('ator$', 'ate', word1)
        # indras->indra
        word1 = re.sub('s$', '', word1)
        # perceptibility->perceptible
        word1 = re.sub('tibility$', 'tible', word1)
        # connexion->connection
        word1 = re.sub('exion$', 'ection', word1)
        # besprinkle->sprinkle
        word1 = re.sub('^be', '', word1)
        # deputyship->deputy
        word1 = re.sub('ship$', '', word1)
        if word1 == '':
            return False
        else:
            result = base_dict.check(word1)
            return result
    return result


def find_abnormal_english_words(xmlfile, logfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    entries = root.findall('./H1')
    flog = codecs.open(logfile, 'w', 'utf-8')

    result = []
    for entry in entries:
        lnum = entry.find('./tail/L')
        key1 = entry.find('./h/key1')
        body = entry.find('./body')
        line = ET.tostring(body, encoding="unicode")
        """
        if key1.text == 'akza':
            print(line)
        """
        # Ignore the initial Anglicised Sanskrit part.
        line = ignore_anglicised_sanskrit(line, identifier)
        # Ignore page numbers like [Page114-b+ 50]
        # See https://github.com/sanskrit-lexicon/csl-corrections/issues/28
        line = re.sub(r'\[Page[^\]]*\]', '', line)
        # YAT - apoha - ascertain- <br />ment
        # toge-  [Page209-b+ 38] <br/>ther;
        line = re.sub(r'<br />', '', line)
        """
        if 'The ascertain' in line:
            print(line)
            exit(0)
        """
        # MW - atI -    <s>atI<srs />yate</s>
        line = line.replace('<srs />', '')
        # MW - <shortlong/>
        line = line.replace('<shortlong />', '')
        # AE - acid - <b>-ify,</b>
        line = re.sub(r'<b>\-[^<]*</b>', '', line)
        # AE - baton - <b>Batoon,</b>
        # AE - anarchy - <b>Anarch, Anar-</b>
        line = re.sub(r'<b>[^,\-]*[,\-]</b>', '', line)
        line = exclude_tags(line, tagsToExclude)
        words = return_ascii_words(line)
        words = [a for a in words if not verify_word(a, base_dict)]
        joinedwords = ','.join(words)
        # suggestions = [base_dict.suggest(a)[0] for a in words]
        # joinedsuggestions = ','.join(suggestions)
        if len(words) > 0:
            joinedwords = ','.join(words)
            result.append((lnum.text, key1.text, joinedwords))
            if key1.text != joinedwords.lower():
                print(lnum.text)
                print(key1.text)
                print(joinedwords)
                # print(joinedsuggestions)
                print()
                # flog.write(lnum.text + ':' + key1.text + ':' + joinedwords + ':' + joinedsuggestions + '\n')
                flog.write(lnum.text + ':' + key1.text + ':' + joinedwords + '\n')
    flog.close()
    return result


def prepare_sanskrit_dict(fileins, fileout):
    fout = codecs.open(fileout, 'w', 'utf-8')
    for filein in fileins:
        fin = codecs.open(filein, 'r', 'utf-8')
        for line in fin:
            splt = re.split(r':', line)
            headword = splt[0].rstrip()
            fout.write(headword + '\n')
            fout.write(sanscript.transliterate(headword, 'slp1', 'itrans') + '\n')
        fin.close()
    fout.close()


if __name__ == "__main__":
    # prepare_sanskrit_dict(['sanhw1.txt', 'mwb.txt'], 'sanskrit_dict.txt')
    base_dict = enchant.DictWithPWL('en_UK', 'sanskrit_dict.txt')
    # dictsWithEnglish = ['vei']
    for code in dictsWithEnglish:
        # code = sys.argv[1]
        # code = code.lower()
        xmlfile = os.path.join('/var/www/html/cologne', code, 'pywork', code + '.xml')
        logfile = os.path.join('output', code + '_error.txt')
        tagsToExclude = sanskritTags[code]
        identifier = startIdentifier[code]
        result = find_abnormal_english_words(xmlfile, logfile)
        # print(result)
