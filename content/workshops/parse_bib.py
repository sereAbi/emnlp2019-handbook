org = open('organizers','r').readlines()
name = open('names','r').readlines()
for i in range(0,14):
    orgs=map(lambda x: '%s, %s'%(x.split(' ')[1], x.split(' ')[0]) ,org[i].strip().split('|'))
    print('@INPROCEEDINGS{workshop%s,'%(i+1))
    print('  title={%s},'%name[i].strip())
    print('  author= {%s},'%' and '.join(orgs))
    print('  sortname= {%s}'%' and '.join(orgs))
    print('}')

