# -*- coding: utf-8 -*-
"""Find potential errors in the English description in Cologne dictionaries.

Author - drdhaval2785@gmail.com
Date - 01 January 2021

Usage - python3 find_english_errors.py

Prerequisites -
1. Cologne dictionaries are installed in local installation at /var/www/html/cologne e.g. /var/www/html/cologne/mw
2. CORRECTIONS repository is placed at /var/www/html/cologne/CORRECTIONS.
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
    """Ignore the initial non-english text based on startIdentifier."""
    if identifier != '':
        line = re.sub('^[^' + identifier + ']*' + identifier, '', line)
    return line


def exclude_tags(line, tagsToExclude):
    """Remove text between tagsToExclude for given dictionary."""

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
    """Return only proper ASCII words."""
    # This function removes IAST or foreign language words.
    # split the line into splits.
    splits = re.split(r'[ ;,\?\.\!\_—]', line)
    # Initialize the output list
    words = []
    # For each split in splits list,
    for split in splits:
        # If there is a hyphen in the split, we need to check
        # whether both the components are proper words.
        m = re.split(r'[\-]+', split)
        # Remove empty strings.
        # https://stackoverflow.com/questions/3845423/remove-empty-strings-from-a-list-of-strings
        m = list(filter(None, m))
        # If items separated by hyphen are proper words, split them.
        # Otherwise remove the hyphen and join them.
        if len(m) > 1:
            if all(verify_word(a, base_dict) for a in m):
                # Add to the output list.
                words += m
        # If there is no hypen, then continue further.
        elif re.search('^[\x00-\x7F]+$', split):
            # split by any non text item.
            split = re.sub('[^a-zA-Z]', '', split)
            # Ignore blank entries and entries starting with capital letters.
            # See https://github.com/sanskrit-lexicon/csl-corrections/issues/28#issuecomment-753334079
            if split != '' and not re.search('^[A-Z]', split):
                # Append to the output list
                words.append(split)
    # return output list.
    return words


def verify_word(word, base_dict):
    """Verify whether a word can be made from base_dict."""
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
        # False if the word1 is an empty string.
        if word1 == '':
            return False
        else:
            # Check whether the word is in the dictionary.
            result = base_dict.check(word1)
            return result
    return result


def find_abnormal_english_words(xmlfile, logfile):
    """Find abnormal entlish words from xmlfile and store in logfile."""
    # parse xmlfile
    tree = ET.parse(xmlfile)
    # Find headword entries
    root = tree.getroot()
    entries = root.findall('./H1')
    # Open logfile to write.
    flog = codecs.open(logfile, 'w', 'utf-8')
    # Initialise blank result list.
    result = []
    # For every entry,
    for entry in entries:
        # Find out lnum, key1, key2
        lnum = entry.find('./tail/L')
        key1 = entry.find('./h/key1')
        body = entry.find('./body')
        # Convert the body to unicode string, for further manipulation.
        line = ET.tostring(body, encoding="unicode")
        # Ignore the initial Anglicised Sanskrit part.
        line = ignore_anglicised_sanskrit(line, identifier)
        # Ignore page numbers like [Page114-b+ 50]
        # See https://github.com/sanskrit-lexicon/csl-corrections/issues/28
        line = re.sub(r'\[Page[^\]]*\]', '', line)
        # YAT - apoha - ascertain- <br />ment
        # toge-  [Page209-b+ 38] <br/>ther;
        line = re.sub(r'<br />', '', line)
        # MW - atI -    <s>atI<srs />yate</s>
        line = line.replace('<srs />', '')
        # MW - <shortlong/>
        line = line.replace('<shortlong />', '')
        # AE - acid - <b>-ify,</b>
        line = re.sub(r'<b>\-[^<]*</b>', '', line)
        # AE - baton - <b>Batoon,</b>
        # AE - anarchy - <b>Anarch, Anar-</b>
        line = re.sub(r'<b>[^,\-]*[,\-]</b>', '', line)
        # Remove the text between the tagsToExclude.
        line = exclude_tags(line, tagsToExclude)
        # Find ASCII words from the given line.
        words = return_ascii_words(line)
        # Keep only the words which are failing in pyenchant dictionary check.
        words = [a for a in words if not verify_word(a, base_dict)]
        # Join the suspect words by comma.
        joinedwords = ','.join(words)

        # If there are suspect words,
        if len(words) > 0:
            # Append (lnum, key1, joinedwords) tuple to the result list.
            result.append((lnum.text, key1.text, joinedwords))
            # If joinedwords is equal to key1, nothing remains to be done.
            # If not, note it in the logfile.
            if key1.text != joinedwords.lower():
                # Display console message to user.
                print(lnum.text)
                print(key1.text)
                print(joinedwords)
                print()
                # Write to logfile.
                flog.write(lnum.text + ':' + key1.text + ':' + joinedwords + '\n')
    # Close the file
    flog.close()
    # Return result to the caller function.
    return result


def prepare_sanskrit_dict(fileins, fileout):
    """Prepare sanskrit dictionary.

    Not needed to be used frequently."""
    # Initialize output file.
    fout = codecs.open(fileout, 'w', 'utf-8')
    # For all input files,
    for filein in fileins:
        # Open input file.
        fin = codecs.open(filein, 'r', 'utf-8')
        # For each line,
        for line in fin:
            splt = re.split(r':', line)
            # headword is before the colon mark.
            headword = splt[0].rstrip()
            # Write SLP1 headword.
            fout.write(headword + '\n')
            # Convert and write headword into itrans too.
            fout.write(sanscript.transliterate(headword, 'slp1', 'itrans') + '\n')
        # Close input file.
        fin.close()
    # Close output file.
    fout.close()


if __name__ == "__main__":
    # Prepare a dictionary with en_UK from pyenchant
    # and sanskrit_dict.txt (which houses headwords in SLP1 and itrans)
    base_dict = enchant.DictWithPWL('en_UK', 'sanskrit_dict.txt')
    # For each dictionary,
    for code in dictsWithEnglish:
        # find out  xxx.xml
        xmlfile = os.path.join('/var/www/html/cologne', code, 'pywork', code + '.xml')
        # Create a file to store the output.
        logfile = os.path.join('output', code + '_error.txt')
        # Find out tags to exclude for that dictionary.
        tagsToExclude = sanskritTags[code]
        # Find out identifier from which content starts 'body' tag of xml.
        identifier = startIdentifier[code]
        # Find abnormal english words from xmlfile and store in logfile
        result = find_abnormal_english_words(xmlfile, logfile)
