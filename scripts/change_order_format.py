import argparse
#import ipdb

parser = argparse.ArgumentParser()
parser.add_argument('order_file')
parser.add_argument('output_file')
args = vars(parser.parse_args())

f1 = open(args['order_file'], 'r')
f2 = open(args['output_file'], 'w')

for line in f1:
	if 'Papers' in line:
		time = line[2:].split(' ', 1)[0]
	elif line.startswith('='):
		name, rest = line[2:].split('(', 2)
		room =  rest[:-3]
		f2.write(' '.join(['=', time, name[:-1], '#', '%room', room, '%chair', 'chairname', '%aff1', 'affname'])+'\n')
	else:
		f2.write(line)


f1.close()
f2.close()

	
