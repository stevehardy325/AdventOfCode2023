import math
import re
import unittest
import os
from datetime import datetime
from multiprocessing import Process, Queue

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
        self.assertEqual(test_answer, 71503)

    def test_parse_line_numbers(self):
        t1, = parse_line_numbers('Time:      7  15   30')
        self.assertEqual(t1, 71530)
        d1, = parse_line_numbers('Distance:  9  40  200')
        self.assertEqual(d1, 940200)

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
        self.assertEqual(calc_possible_wins_optimized(7, 9), 4)
        self.assertEqual(calc_possible_wins_optimized(15, 40), 8)
        self.assertEqual(calc_possible_wins_optimized(30, 200), 9)
        self.assertEqual(calc_possible_wins_naive(7, 9), 4)
        self.assertEqual(calc_possible_wins_naive(15, 40), 8)
        self.assertEqual(calc_possible_wins_naive(30, 200), 9)


################################
#############  Data functions
################################

def parse_line_numbers(s: str):
    numbers = re.findall(r'\d+', s)
    digits_joined = ''.join(numbers)

    return [int(digits_joined)]

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


def calc_possible_wins_naive(runtime: int, target_dist: int) -> int:
    # brute force execution, works but slow
    distances = [calc_distance(t, runtime) for t in range(1,runtime)
                 if calc_distance(t, runtime) > target_dist]

    return len(distances)


def calc_possible_wins_optimized(runtime: int, target_dist: int) -> int:
    # we know that the first half of the answers mirror the second, so only calculate half

    first_possible_distances = [calc_distance(t, runtime) for t in range(1,math.ceil(runtime/2))]
    winners = len([d for d in first_possible_distances if d > target_dist]) * 2

    if runtime % 2 == 0: # even runtimes have a single 'winner' in the middle we have to add
        return winners + 1
    return winners


def get_answer(inputfile, calculation=calc_possible_wins_optimized):
    # answer calculation goes here
    # this is a stub example
    start = datetime.now()

    data_list = get_dataset_lines(inputfile)
    times = parse_line_numbers(data_list[0])
    distances = parse_line_numbers(data_list[1])

    answer = 1

    for i in range(len(times)):
        answer *= calculation(times[i], distances[i])

    end = datetime.now()
    duration = end - start

    print('{} {} {}'.format(times, calculation, duration))

    return answer


################################
#############  Runtime execution
################################

def run_unit_tests():
    testprog = unittest.main(exit=False, verbosity=2)
    error_ct = len(testprog.result.errors)
    fail_ct = len(testprog.result.failures)
    return error_ct < 1 and fail_ct < 1

def get_answer_naive(inputfile):
    return get_answer(inputfile, calculation=calc_possible_wins_naive)

def queue_func_wrapper(funcname, fname, res_q):
    res_q.put(funcname(fname))

def main():
    start = datetime.now()
    test_answer_naive_queue = Queue()
    test_answer_optimized_queue = Queue()
    real_answer_naive_queue = Queue()
    real_answer_optimized_queue = Queue()

    test_answer_naive_proc = Process(target=queue_func_wrapper,
                                     args=(get_answer_naive, test_fname, test_answer_naive_queue))
    real_answer_naive_proc = Process(target=queue_func_wrapper,
                                     args=(get_answer, test_fname, test_answer_optimized_queue))
    test_answer_optimized_proc = Process(target=queue_func_wrapper,
                                         args=(get_answer_naive, input_fname, real_answer_naive_queue))
    real_answer_optimized_proc = Process(target=queue_func_wrapper,
                                         args=(get_answer, input_fname, real_answer_optimized_queue))

    test_answer_naive_proc.start()
    real_answer_naive_proc.start()
    test_answer_optimized_proc.start()
    real_answer_optimized_proc.start()

    test_answer_naive_proc.join()
    real_answer_naive_proc.join()
    test_answer_optimized_proc.join()
    real_answer_optimized_proc.join()

    test_answer = test_answer_optimized_queue.get()
    real_answer = real_answer_optimized_queue.get()

    print('Test answer: {}{}Real answer: {}'.format(test_answer, os.linesep, real_answer))

    end = datetime.now()
    duration = end - start
    print('Took {} to execute all 4 versions'.format(duration))



if __name__ == '__main__':
    succesful_test = run_unit_tests()
    if succesful_test:
        main()
