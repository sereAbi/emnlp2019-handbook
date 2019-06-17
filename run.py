import sys
replace= {}
list = open(sys.argv[1]).readlines()
for i in range(len(list)/3):
    replace[list[i*3+1].strip()] = list[i*3+2].strip()

file = open(sys.argv[2]).readlines()
for line in file:
    for item in replace:
        line = line.replace(item, replace[item])
    print line,

