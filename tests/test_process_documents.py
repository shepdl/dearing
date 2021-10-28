import unittest

from processors import ProcessDocumentStep
from tests.helpers_for_tests import TestHelpers


class TestLongestOverlapReturnsExpectedResults(unittest.TestCase):

    def test_identical_phrases_returns_identical(self):
        input_sentence = 'when in the course of human events it becomes necessary for one people to dissolve the political bonds'.split(' ')
        input_phrase = 'when in the course of human events it becomes necessary for one people to dissolve the political bonds'.split(' ')
        self.assertEqual(input_phrase, ProcessDocumentStep.longest_overlap(input_sentence, input_phrase))

    def test_identical_phrases_with_extra_spaces_returns_identical(self):
        input_sentence = 'when in   the course of human   events    it becomes necessary    for one people to dissolve the political bonds'.split(' ')
        input_phrase = 'when in the course of human events it becomes necessary for one people to dissolve the political bonds'.split(' ')
        self.assertEqual(input_phrase, ProcessDocumentStep.longest_overlap(input_sentence, input_phrase))

    def test_above_overlap_threshold_returns_correct_overlap(self):
        input_sentence = 'when in the course of human events it becomes a place in time and a stitch'.split(' ')
        input_phrase = 'when in the course of human events it becomes necessary for one people to dissolve the political bonds'.split(' ')
        self.assertEqual('when in the course of human events it becomes'.split(' '), ProcessDocumentStep.longest_overlap(input_sentence, input_phrase))


    def test_above_overlap_threshold_with_gap_at_end_does_not_return_overlap(self):
        input_sentence = 'and then sometimes in the course'.split(' ')
        input_phrase = 'when in the course of human events it becomes necessary for one people to dissolve the political bonds'.split(' ')
        self.assertEqual([], ProcessDocumentStep.longest_overlap(input_sentence, input_phrase))

    def test_gap_at_end_of_sentence_pushing_over_overlap_threshold_does_not_result_in_overlap(self):
        input_sentence = 'and then sometimes when in the course'.split(' ')
        input_phrase = 'when in the course of human events it becomes necessary for one people to dissolve the political bonds'.split(' ')
        self.assertEqual([], ProcessDocumentStep.longest_overlap(input_sentence, input_phrase))


class TestPhraseLongEnough(unittest.TestCase, TestHelpers):

    THRESHOLD = 5

    def test_phrase_crosses_threshold_passes(self):
        self.assertTrue(ProcessDocumentStep.is_long_enough(['a', 'a', 'a', 'a', 'a',], 5))

    def test_phrase_crosses_threshold_and_has_gaps_at_beginning_passes(self):
        self.assertTrue(ProcessDocumentStep.is_long_enough([None, None, None, None, 'a', 'a', 'a', 'a', 'a',], 5))

    def test_phrase_crosses_threshold_and_has_gaps_at_end_passes(self):
        self.assertTrue(ProcessDocumentStep.is_long_enough(['a', 'a', 'a', 'a', 'a', None, None, None, None, None,], 5))

    def test_phrase_crosses_threshold_and_has_gaps_at_beginning_and_end_passes(self):
        self.assertTrue(ProcessDocumentStep.is_long_enough([None, None, None, 'a', 'a', 'a', 'a', 'a', None, None, None, None, None,], 5))

    def test_phrase_crosses_threshold_with_gaps_in_middle_fails(self):
        self.assertFalse(ProcessDocumentStep.is_long_enough(['a', 'a', None, None, None, 'a', 'a', ], 5))

    def test_phrase_crosses_threshold_with_gaps_at_end_fails(self):
        self.assertFalse(ProcessDocumentStep.is_long_enough(['a', 'a', 'a', None, None, None, None, None,], 5))

    def test_phrase_crosses_threshold_with_gaps_at_beginning_fails(self):
        self.assertFalse(ProcessDocumentStep.is_long_enough([None, None, None, None, 'a', 'a', 'a',], 5))

    def test_phrase_crosses_threshold_with_2_sets_of_gaps_fails(self):
        self.assertFalse(ProcessDocumentStep.is_long_enough(
            ['a', 'a', 'a', None, None, None, None, None, 'a', None, None, None, None, None, ], 5)
        )



if __name__ == '__main__':
    unittest.main()
