import re
import sys

author_ptn = re.compile(r"^AUTHOR")
sortname_ptn = re.compile(r"^SORTNAME")
# point_ptn = re.compile(r"\. ")

fname = sys.argv[1]

with open('tempfile.txt', 'w') as outfile:
    for line in open(fname, 'r').readlines():
        if re.match(author_ptn, line) or re.match(sortname_ptn, line):
            line = line.replace(", ", " and ")

        outfile.write(line)

