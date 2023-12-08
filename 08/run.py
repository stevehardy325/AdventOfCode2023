"""Advent of Code 2023 Stub file."""
import unittest
import os
import re

TEST_FNAME = 'test.txt'
TEST_FNAME2 = 'test2.txt'
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
        self.assertEqual(test_answer, 2)

    def testExampleAnswer2(self):
        test_answer =get_answer(TEST_FNAME2)
        # validation result for testing goes here
        self.assertEqual(test_answer, 6)

################################
#############  Data functions
################################



def getNodes(s: str):
    start, left, right = re.findall(r'[A-Z]+', s)
    link_dct = {'L': left, 'R': right}

    return start, link_dct


def get_dataset_lines(filename):
    # simple way to get cleaned up data as a list of strings
    # each list item is one text line, normalized to remove newline chars and extra space

    lines = []
    with open(filename) as fobj:
        lines = [ln.strip() for ln in fobj.readlines()]

    return lines


def get_answer(inputfile):
    ''' answer calculation goes here'''

    data_list = get_dataset_lines(inputfile)

    cycle_directions = data_list[0].strip()
    links = data_list[2:]

    node_dct = {}

    for link_str in links:
        start, lr_dct = getNodes(link_str)
        node_dct[start] = lr_dct

    cur_node = 'AAA'
    target_node = 'ZZZ'
    steps = 0

    while target_node != cur_node:
        go_direction = cycle_directions[steps % len(cycle_directions)]
        cur_node = node_dct[cur_node][go_direction]
        steps += 1



    return steps


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
