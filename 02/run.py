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
        self.assertEqual(test_answer, 8)


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

def checkNumColorValid(n: int, color: str) -> bool:
    max_dict = {'red': 12, 'green': 13, 'blue': 14}
    return n <= max_dict[color]

def checkColorStrValid(s: str) -> bool:
    # '3 blue'
    n_str, color = s.split(' ')
    return checkNumColorValid(int(n_str), color)

def checkSetStrValid(s: str) -> bool:
    # '3 blue, 4 red'
    for color_str in s.split(', '):
        if not checkColorStrValid(color_str):
            return False
    return True

def checkGameStrValid(s: str) -> bool:
    # 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    for set_str in s.split('; '):
        if not checkSetStrValid(set_str):
            return False
    return True


def getLineTotalAdd(s: str) -> bool:
    # Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    game_num_str, game_str = s.split(': ')
    game_num_int = int(game_num_str.split(' ')[-1])

    if checkGameStrValid(game_str):
        return game_num_int
    else:
        return 0


def get_answer(inputfile):
    # answer calculation goes here

    data_list = get_dataset_lines(inputfile)
    answer = sum(getLineTotalAdd(l) for l in data_list)

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
