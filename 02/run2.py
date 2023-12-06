import unittest
import os
from collections import defaultdict

test_fname = 'test.txt'
input_fname = 'input.txt'

################################
#############  Unit tests
################################

class TestFilesExistMethod(unittest.TestCase):
    # validate that necessary files are present in current working directory
    def assertFileExists(self, path):
        if not os.path.isfile(path):
            raise AssertionError("File does not exist: {}".format(os.path.abspath(path)))

    def testTestInputFileExists(self):
        self.assertFileExists(test_fname)

    def testRealInputFileExists(self):
        self.assertFileExists(input_fname)

class TestAnswerMethod(unittest.TestCase):
    # unit testing for answer validation
    def testExampleAnswer(self):
        test_answer =get_answer(test_fname)
        # validation result for testing goes here
        self.assertEqual(test_answer, 2286)


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


def getMinColorsFromColorStr(s: str):
    # '3 blue'
    n_str, color = s.split(' ')
    return int(n_str), color

def getMinColorsFromSetStr(s: str):
    # '3 blue, 4 red'
    min_colors = defaultdict(lambda: 0)
    for color_str in s.split(', '):
        n, color = getMinColorsFromColorStr(color_str)
        min_colors[color] = n
    return min_colors

def getMinColorsFromGameStr(s: str) -> bool:
    # 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    min_colors = defaultdict(lambda: 0)

    for set_str in s.split('; '):
        newest_min_colors = getMinColorsFromSetStr(set_str)
        for c in ['red', 'green', 'blue']:
            if newest_min_colors[c] > min_colors[c]:
                min_colors[c] = newest_min_colors[c]

    return min_colors

def getLinePowerAdd(s: str) -> bool:
    # Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    _, game_str = s.split(': ')

    min_colors = getMinColorsFromGameStr(game_str)
    power = 1
    for c in ['red', 'green', 'blue']:
        power *= min_colors[c]

    return power



def get_answer(inputfile):
    # answer calculation goes here
    # this is a stub example

    data_list = get_dataset_lines(inputfile)
    answer = sum(getLinePowerAdd(l) for l in data_list)

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
    test_answer = get_answer(test_fname)
    real_answer = get_answer(input_fname)

    print('Test answer: {}{}Real answer: {}'.format(test_answer, os.linesep, real_answer))

if __name__ == '__main__':
    succesful_test = run_unit_tests()
    if succesful_test:
        main()
