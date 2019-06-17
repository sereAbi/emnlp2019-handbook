import sys
a = open(sys.argv[1]).readlines()
b = open(sys.argv[2]).readlines()
list = []
for item in b:
    if item.startswith('='):
        list.append(item)
i = 0
for id, item in enumerate(a):
    if item.startswith('='):
        print list[i],
        i+=1
    else:
        print a[id],
