import re
import unittest
import os

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
        self.assertEqual(test_answer, 288)

    def testLineInput(self):
        t1, t2, t3 = parse_line_numbers('Time:      7  15   30')
        self.assertEqual(t1, 7)
        self.assertEqual(t2, 15)
        self.assertEqual(t3, 30)
        d1, d2, d3 = parse_line_numbers('Distance:  9  40  200')
        self.assertEqual(d1, 9)
        self.assertEqual(d2, 40)
        self.assertEqual(d3, 200)

    def test_calc_distance(self):
        d0, d1, d2, d3, d4, d5, d6, d7, d8 = [calc_distance(t, 7) for t in range(9)]
        self.assertEqual(d0, 0)
        self.assertEqual(d1, 6)
        self.assertEqual(d2, 10)
        self.assertEqual(d3, 12)
        self.assertEqual(d4, 12)
        self.assertEqual(d5, 10)
        self.assertEqual(d6, 6)
        self.assertEqual(d7, 0)
        self.assertEqual(d8, 0)

    def test_calc_possible_wins(self):
        self.assertEqual(calc_possible_wins(7, 9), 4)
        self.assertEqual(calc_possible_wins(15, 40), 8)
        self.assertEqual(calc_possible_wins(30, 200), 9)


################################
#############  Data functions
################################

def parse_line_numbers(s: str):
    numbers = re.findall('\d+', s)
    int_numbers = [int(n) for n in numbers]

    return int_numbers

def get_dataset_lines(filename):
    # simple way to get cleaned up data as a list of strings
    # each list item is one text line, normalized to remove newline chars and extra space

    lines = []
    with open(filename) as fobj:
        lines = [ln.strip() for ln in fobj.readlines()]
        
    return lines

def calc_distance(time_held: int, runtime: int):
    if time_held <= 0 or time_held >= runtime:
        return 0
    else:
        return time_held*(runtime-time_held)

def calc_possible_wins(runtime: int, target_dist: int) -> int:
    possible_distances = [calc_distance(t, runtime) for t in range(1,runtime)]
    return len([calc_distance(t, runtime) for t in range(1,runtime) if calc_distance(t, runtime) > target_dist])
    

def get_answer(inputfile):
    # answer calculation goes here 
    # this is a stub example 

    data_list = get_dataset_lines(inputfile)
    times = parse_line_numbers(data_list[0])
    distances = parse_line_numbers(data_list[1])

    answer = 1

    for i in range(len(times)):
        answer *= calc_possible_wins(times[i], distances[i])

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