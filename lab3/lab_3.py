import os

INPUTS_DIR = 'inputs/'
FILES = os.listdir(INPUTS_DIR)


def bits(path):
	with open(path, 'rb') as f:
		bytes = (ord(b) for b in f.read())
		for b in bytes:
			for i in xrange(0, 8):
				yield (b >> i) & 1



b = bits(INPUTS_DIR + FILES[0])

for i in b:
	print i


