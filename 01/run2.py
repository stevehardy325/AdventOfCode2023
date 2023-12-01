import unittest
import os
import re

test_fname = 'test2.txt'
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
        self.assertEqual(test_answer, 281)

    def testTextToInt(self):
        self.assertEqual(convertTextToNum('one'), 1)
        self.assertEqual(convertTextToNum('TWO'), 2)
        self.assertEqual(convertTextToNum('thrEe'),3)
        self.assertEqual(convertTextToNum('four'),4)
        self.assertEqual(convertTextToNum('five'),5)
        self.assertEqual(convertTextToNum('six'),6)
        self.assertEqual(convertTextToNum('seven'),7)
        self.assertEqual(convertTextToNum('eight'),8)
        self.assertEqual(convertTextToNum('nine'),9)
        self.assertEqual(convertTextToNum('zero'),0)

    def testGetFirstLastNumFromStr(self):
        self.assertEqual(getFirstLastNumFromStr('two1nine'),29)
        self.assertEqual(getFirstLastNumFromStr('eightwothree'),83)
        self.assertEqual(getFirstLastNumFromStr('abcone2threexyz'),13)
        self.assertEqual(getFirstLastNumFromStr('xtwone3four'),24)
        self.assertEqual(getFirstLastNumFromStr('4nineeightseven2'),42)
        self.assertEqual(getFirstLastNumFromStr('zoneight234'),14)
        self.assertEqual(getFirstLastNumFromStr('7pqrstsixteen'),76)

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

def convertTextToNum(s: str) -> int:
    try:
        return int(s)
    except:
        s = s.lower()
        spelled_dict = {
            'one': 1,
            'two': 2,
            'three':3,
            'four':4,
            'five':5,
            'six':6,
            'seven':7,
            'eight':8,
            'nine':9,
            'zero':0
        }
        try:
            return spelled_dict[s.lower()]
        except:
            raise Exception('{} is not a number?', s)

def getFirstLastNumFromStr(s: str) -> int:
    # originally used the following, but the description didn't specify what to do for overlapping
    # ...it turns out that overlapping was required, so regex modified
    # digits = re.findall('(\d|one|two|one|two|three|four|five|six|seven|eight|nine|zero)', s, )
    digits = re.findall('(?=(\d|one|two|one|two|three|four|five|six|seven|eight|nine|zero))', s)
    firstNum = convertTextToNum(digits[0])
    lastNum = convertTextToNum(digits[-1])

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