import os

from tests import RandomExcursionsTest, BinaryMatriceTest

INPUTS_DIR = 'inputs/'
FILES = os.listdir(INPUTS_DIR)

for i, file in enumerate(FILES):
    print 'Start test of {0} file'.format(file)
    result = 'Passed'
    try:
        # results = RandomExcursionsTest.test_input(INPUTS_DIR + file)
        results = BinaryMatriceTest.test_input(INPUTS_DIR + file)
    except ValueError as e:
        result = ''
        print 'File {0} has a bad J (less than 500.)'.format(file)

    with open('{0}-1.txt'.format(i + 1), 'w') as f:
        f.write(str(results))

print 'Tests finished'
