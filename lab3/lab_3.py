import os

from tests import RandomExcursionsTest

INPUTS_DIR = 'inputs/'
FILES = os.listdir(INPUTS_DIR)

for i, file in enumerate(FILES):
    print 'Start test of {0} file'.format(file)
    try:
        results = RandomExcursionsTest.test_input(INPUTS_DIR + file)
    except ValueError as e:
        print 'File {0} has a bad J (less than 500.)'.format(file)
        continue

    with open('{0}.txt'.format(i), 'w') as f:
        f.write(str(results))

print 'Tests finished'





