import sys
lines = open(sys.argv[1]).readlines()
papers = {}
paper = None
for item in lines:
    if 'INPROCEEDINGS' in item: 
        paper = item.split('-')[1][:-2].strip()
        while paper[0] == '0':
            paper = paper[1:]
    elif 'TITLE' in item:
        title = item.split('= {')[1][:-3].strip()
        papers[paper] = title
lines = open(sys.argv[2]).readlines()
papers2 = {}
for item in lines:
    if '#' in item:
        paper = item.split(' ')[0]
        papers2[paper] = item.split('# ')[1].strip()

for item in papers:
    if papers[item].lower() != papers2[item].lower():
        print item
        print papers[item]
        print papers2[item]
