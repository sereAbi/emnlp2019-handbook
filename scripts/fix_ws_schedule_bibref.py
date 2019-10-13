import os
import re

for root, subd, files in os.walk('auto'):
    for f in files:
        if f == 'schedule.tex':
            tmp = 'temp.tex'
            fname = os.path.join(root, f)
            with open(tmp, 'w') as out:
                with open(fname, 'r') as in_:
                    for line in in_.readlines():
                        if re.search('wspaperentry', line):
                            name = line.split('wspaperentry')[1]
                            ws, id_ = name.replace('{', '').replace('}', '').split('-')
                            newname = '{{{}-{}}}'.format(ws.strip(), int(id_))
                            out.write(line.replace(name, newname) + '\n')
                        else:
                            out.write(line)
            os.rename(tmp, fname)
            print(fname, 'done')
