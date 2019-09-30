import sys
import re
from bs4 import BeautifulSoup                                                                                 
import unicodedata
import os

def latex_escape(str_):
    """Replaces unescaped special characters with escaped versions, and does
    other special character conversions."""
    
    str_ = str_.replace('~','{\\textasciitilde}')

    # escape these characters if not already escaped
    special_chars = r'\#\@\&\$\_\%'
    patternstr = r'([^\\])([%s])' % (special_chars)
    str_ = re.sub(patternstr, '\\1\\\\\\2', str_)

    return str_

tag = sys.argv[1]

try:
    os.makedirs('auto/{}'.format(tag))
except FileExistsError:
    pass

try:
    os.makedirs('auto/abstracts')
except FileExistsError:
    pass
    
metadata = []

for fname in os.listdir('data/{}/proceedings/accepted'.format(tag)):
    if fname == 'accepted.html':
        continue
    else:
        id_ = int(os.path.splitext(fname)[0])
        f = 'data/{}/proceedings/accepted/{}'.format(tag, fname)
        soup = BeautifulSoup(open(f, 'r'), features='lxml')                 
        title = latex_escape(soup.h2.string)
        authors = latex_escape(soup.h3.string)
        
        mdata = "@INPROCEEDINGS{{ {}-{},\n".format(tag, id_)
        mdata += "AUTHOR = {{ {} }},\n".format(authors)
        mdata += "SORTNAME = {{ {} }},\n".format(''.join([str(c) for c in unicodedata.normalize('NFD', str(authors)) if unicodedata.category(c) != 'Mn']))
        mdata += "TITLE = {{ {} }},\n".format(title)
        mdata += "}\n"
        metadata.append(mdata)

        if tag == 'papers':
            for text in soup.findAll('h2'):
                if text.string == 'Abstract':
                    abstract = latex_escape(text.next_sibling.string).strip()
                    with open('auto/abstracts/{}-{}.tex'.format(tag, id_), 'w') as abstract_file:
                        abstract_file.write(abstract)
            
with open('auto/{}/papers.bib'.format(tag), 'w', encoding='utf-8') as bibfile:
    for m in metadata:
        bibfile.write(m)
