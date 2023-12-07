"""Advent of Code 2023 Stub file."""
from functools import cmp_to_key
import math
import unittest
import os
from collections import defaultdict

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
        self.assertEqual(test_answer, 5905)

    def testgetHandRank(self):
        self.assertEqual(getHandRank('23456'), 1)
        self.assertEqual(getHandRank('32T3K'), 2)
        self.assertEqual(getHandRank('KK677'), 2.5)
        self.assertEqual(getHandRank('TTT23'), 3)
        self.assertEqual(getHandRank('TTT22'), 3.5)
        self.assertEqual(getHandRank('QQQJA'), 4)
        self.assertEqual(getHandRank('QQQQQ'), 5)

        self.assertEqual(getHandRank('2244J'), 3.5)

        self.assertEqual(getHandRank('2344J'), 3)
        self.assertEqual(getHandRank('234JJ'), 3)

        self.assertEqual(getHandRank('2333J'), 4)
        self.assertEqual(getHandRank('233JJ'), 4)
        self.assertEqual(getHandRank('23JJJ'), 4)

        self.assertEqual(getHandRank('2222J'), 5)
        self.assertEqual(getHandRank('222JJ'), 5)
        self.assertEqual(getHandRank('22JJJ'), 5)
        self.assertEqual(getHandRank('2JJJJ'), 5)
        self.assertEqual(getHandRank('JJJJJ'), 5)

    def testcompareHandCards(self):
        self.assertEqual(compareHandCards('KK677', 'KTJJT'), 1)
        self.assertEqual(compareHandCards('T55J5', 'QQQJA'), -1)
        self.assertEqual(compareHandCards('QQQJA', 'QQQJA'), 0)

    def testcompareHands(self):
        self.assertEqual(compareHands('32T3K', '32T3K'), 0)
        self.assertEqual(compareHands('KK677', '32T3K'), 1)
        self.assertEqual(compareHands('32T3K', 'KK677'), -1)

################################
#############  Data functions
################################

def getHandRank(s: str) -> int:
    # calculate hand rank based on type of pairs etc

    counts = defaultdict(lambda: 0)
    for card in s:
        counts[card] += 1
        

    fives = 0
    fours = 0
    threes = 0
    pairs = 0

    for card, count in counts.items():
        if card != 'J':
            if count == 5:
                fives += 1
            elif count == 4:
                fours += 1
            elif count == 3:
                threes += 1
            elif count == 2:
                pairs += 1

    if fives > 0 or counts['J'] == 5:
        return 5
    elif fours > 0:
        return 4 + counts['J']
    elif threes > 0:
        if pairs > 0:
            return 3.5 #full house
        else:
            return 3 + counts['J']
    elif pairs == 2:
        return 2.5 + counts['J'] #2 pairs
    elif pairs == 1:
        return 2 + counts['J']
    return 1 + counts['J']

def getCardRank(s: str) -> int:
    # get numerically comparable rank for each card, including faces

    face_cards = {'T': 10, 'J': 1, 'Q': 12, 'K': 13, 'A': 14}
    try:
        return int(s)
    except ValueError:
        return face_cards[s]

def compareHandCards(s1: str, s2: str) -> int:
    # compare ranks of cards in hand, from left to right

    for card1, card2 in zip(s1, s2):
        card1_rank = getCardRank(card1)
        card2_rank = getCardRank(card2)

        if card1_rank > card2_rank:
            return 1
        elif card1_rank < card2_rank:
            return -1
        
    return 0

def compareHands(s1: str, s2: str) -> int:
    # compare hands using Hand Rank, and fall back to comparing by high card

    h1 = getHandRank(s1)
    h2 = getHandRank(s2)

    if h1 < h2:
        return -1
    elif h1 > h2:
        return 1
    
    return compareHandCards(s1, s2)



def get_dataset_lines(filename):
    # simple way to get cleaned up data as a list of strings
    # each list item is one text line, normalized to remove newline chars and extra space

    lines = []
    with open(filename) as fobj:
        lines = [ln.strip() for ln in fobj.readlines()]

    return lines


def get_answer(inputfile):
    ''' answer calculation goes here '''
    
    data_list = get_dataset_lines(inputfile)

    hands = []
    bets = {}

    for l in data_list:
        hand, bet = l.split(' ')
        hands += [hand]
        bets[hand] = int(bet)

    hands_sorted = sorted(hands, key=cmp_to_key(compareHands))
    bets_sorted = [bets[h] for h in hands_sorted]
    
    winnings = 0
    for bet, rank in zip(bets_sorted, range(1, len(bets_sorted) + 1)):
        winnings += bet * rank


    answer = '!'.join(data_list)

    return winnings


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
