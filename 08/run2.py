"""Advent of Code 2023 Stub file."""
from datetime import datetime
from functools import cache
import math
import unittest
import os
import re

TEST_FNAME = 'test3.txt'
INPUT_FNAME = 'input.txt'

NODE_DCT = {}
cycle_directions = ''

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
        test_answer =get_answer_optimized(TEST_FNAME)
        # validation result for testing goes here
        self.assertEqual(test_answer, 6)

    '''def testExampleAnswer2(self):
        test_answer =get_answer(TEST_FNAME2)
        # validation result for testing goes here
        self.assertEqual(test_answer, 6)'''

################################
#############  Data functions
################################



def getNodes(s: str):
    start, left, right = re.findall(r'[A-Z0-9]+', s)
    link_dct = {'L': left, 'R': right}

    return start, link_dct


def get_dataset_lines(filename):
    # simple way to get cleaned up data as a list of strings
    # each list item is one text line, normalized to remove newline chars and extra space

    lines = []
    with open(filename) as fobj:
        lines = [ln.strip() for ln in fobj.readlines()]

    return lines



@cache
def stepsToNextZ(start_node: str, cycle_position: int):
    cur_node = start_node
    additional_steps = 0

    while additional_steps == 0 or cur_node[2] != 'Z':
        go_direction = cycle_directions[(cycle_position + additional_steps) % len(cycle_directions)]
        cur_node = NODE_DCT[cur_node][go_direction]
        additional_steps += 1

    return additional_steps, cur_node

def get_answer_optimized(inputfile):
    ''' Each set of start/ends cycles for X steps in the step-through and only goes through 1 valid Z-ending node
    
        Therefore the LCM of all cycle times is the length for all cycles to complete simultaneously
    '''

    starttime = datetime.now()

    data_list = get_dataset_lines(inputfile)

    global cycle_directions
    cycle_directions = data_list[0].strip()
    links = data_list[2:]

    global NODE_DCT
    NODE_DCT = {}

    for link_str in links:
        start, lr_dct = getNodes(link_str)
        NODE_DCT[start] = lr_dct

    cur_nodes = [n for n in NODE_DCT.keys() if n[2] == 'A']

    z_steps = [0 for n in cur_nodes]

    for i, node in enumerate(cur_nodes):
        steps_to_z_ending, _ = stepsToNextZ(node, 0)
        z_steps[i] = steps_to_z_ending


    end = datetime.now()
    print(end - starttime)

    answer = math.lcm(*z_steps)

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
    test_answer = get_answer_optimized(TEST_FNAME)
    real_answer = get_answer_optimized(INPUT_FNAME)    

    print('Test answer: {}{}Real answer: {}'.format(test_answer, os.linesep, real_answer))

if __name__ == '__main__':
    succesful_test = run_unit_tests()
    if succesful_test:
        main()
