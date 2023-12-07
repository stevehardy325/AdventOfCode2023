"""Advent of Code 2023 Stub file."""
import unittest
import os

TEST_FNAME = 'test.txt'
INPUT_FNAME = 'input.txt'

################################
#############  Unit tests
################################

class TestFilesExistMethod(unittest.TestCase):
    ''' validate that necessary files are present in current working directory '''

    def assertFileExists(self, path):
        '''wrapper to check if a file exists in the filesystem'''

        if not os.path.isfile(path):
            raise AssertionError("File does not exist: {}".format(os.path.abspath(path)))

    def testTestInputFileExists(self):
        self.assertFileExists(TEST_FNAME)

    def testRealInputFileExists(self):
        self.assertFileExists(INPUT_FNAME)

class TestAnswerMethod(unittest.TestCase):
    # unit testing for answer validation
    def testExampleAnswer(self):
        test_answer =get_answer(TEST_FNAME)
        # validation result for testing goes here
        self.assertEqual(test_answer, 'test!input!goes!here')

################################
#############  Data functions
################################

def get_dataset_lines(filename):
    # simple way to get cleaned up data as a list of strings
    # each list item is one text line, normalized to remove newline chars and extra space

    lines = []
    with open(filename) as fobj:
        lines = [ln.strip() for ln in fobj.readlines()]

    return lines


def get_answer(inputfile):
    ''' answer calculation goes here
        this is a stub example'''

    data_list = get_dataset_lines(inputfile)
    answer = '!'.join(data_list)

    return answer


################################
#############  Runtime execution
################################

def run_unit_tests():
    testprog = unittest.main(exit=False, verbosity=2)
    error_ct = len(testprog.result.errors)
    fail_ct = len(testprog.result.failures)
    return error_ct < 1 and fail_ct < 1

def main():
    test_answer = get_answer(TEST_FNAME)
    real_answer = get_answer(INPUT_FNAME)

    print('Test answer: {}{}Real answer: {}'.format(test_answer, os.linesep, real_answer))

if __name__ == '__main__':
    succesful_test = run_unit_tests()
    if succesful_test:
        main()
