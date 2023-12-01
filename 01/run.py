import unittest
import os
import re

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
        self.assertEqual(test_answer, 142)

    def testGetFirstLastNumFromStr(self):
        self.assertEqual(getFirstLastNumFromStr('1abc2'),12)
        self.assertEqual(getFirstLastNumFromStr('pqr3stu8vwx'),38)
        self.assertEqual(getFirstLastNumFromStr('a1b2c3d4e5f'),15)
        self.assertEqual(getFirstLastNumFromStr('treb7uchet'),77)

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

def getFirstLastNumFromStr(s: str) -> int:
    digits = re.findall('\d', s)
    firstNum = digits[0]
    lastNum = digits[-1]
    combined = '{}{}'.format(firstNum, lastNum)
    numAsInt = int(combined)
    return numAsInt


def get_answer(inputfile):
    # answer calculation goes here 
    # this is a stub example 

    data_list = get_dataset_lines(inputfile)
    answer = sum([getFirstLastNumFromStr(s) for s in data_list])

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