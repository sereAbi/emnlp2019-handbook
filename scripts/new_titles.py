import re
from itertools import islice
from collections import namedtuple

paper = re.compile(r"^\d{1,4} \d\d:\d\d--\d\d:\d\d\ #")
poster = re.compile(r"^\d{1,4}\ #")
demo = re.compile('^DEMO')

orderfile = 'data/papers/proceedings/order'
bib = 'auto/papers/papers.bib'
demobib = 'auto/demos/papers.bib'

orderdic = {}
for f in open(orderfile, 'r').readlines():
    if re.match(paper, f) or re.match(poster, f):
        id_, title = f.split('#')
        ref = 'papers-{}'.format(id_.split()[0])
        title = title.strip()
        # print(ref, title)
        orderdic[ref] = title
    # elif re.match(demo, f):
    #     id_, title = f.split('#')
    #     ref = 'demos-{}'.format(id_.split()[0])
    #     # print(ref, title)
    #     orderdic[ref] = title
    else:
        continue

bibdic = {}
bibentry = namedtuple('bibentry', ['ref', 'author', 'sortnames', 'title', 'end'])
with open(bib, 'r') as infile:
    try:
        while True:
            data = islice(infile, 0, 5)
            b = bibentry(*data)
            ref = b.ref[b.ref.find('{ ') + 1: b.ref.find(',')].strip()
            title = b.title[b.title.find('{')+1:b.title.find('}')].strip()
            bibdic[ref] = title
    except StopIteration:
        pass
    except TypeError:
        pass # end

u = 0
c = 0
for k, v in orderdic.items():
    try:
        if v == bibdic[k]:
            u += 1
        else:
            c += 1
    except KeyError:
        print('{} not in bib'.format(k))

print('uguali', u)
print('diversi', c)