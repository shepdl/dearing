import unittest

from processors.update_dictionary_step import Generalizer
from tests.helpers_for_tests import TestHelpers


class PhraseIsGeneralizationTestCase(unittest.TestCase, TestHelpers):

    def test_simple_phrase_is_generalization_with_one_slot(self):
        instance = Generalizer(0.5)
        pattern_phrase = 'to be or not to _ that is the question'.split(' ')
        other_phrase = 'to be or not to be that is the question'.split(' ')
        self.assertTrue(instance.phrase_is_generalization(pattern_phrase, other_phrase))

    def test_simple_phrase_is_generalization_with_two_slots(self):
        instance = Generalizer(0.5)
        pattern_phrase = 'to _ or not to _ that is the question'.split(' ')
        other_phrase = 'to be or not to be that is the question'.split(' ')
        self.assertTrue(instance.phrase_is_generalization(pattern_phrase, other_phrase))

    def test_simple_phrase_is_generalization_with_3_continuous_slots(self):
        instance = Generalizer(0.5)
        pattern_phrase = 'to boldly go where _ _ _ gone'.split(' ')
        other_phrase = 'to boldly go where no one has gone'.split(' ')
        self.assertTrue(instance.phrase_is_generalization(pattern_phrase, other_phrase))

    def test_generalization_works_when_under_length_difference_threshold(self):
        instance = Generalizer(0.5)
        pattern_phrase = 'to boldly go where no one has'.split(' ')
        other_phrase = 'to boldly go where no one has gone'.split(' ')
        self.assertTrue(instance.phrase_is_generalization(pattern_phrase, other_phrase))

    def test_generalization_fails_when_over_length_difference_threshold(self):
        instance = Generalizer(0.5)
        pattern_phrase = 'to boldly go where no '.split(' ')
        other_phrase = 'to boldly go where no one has gone'.split(' ')
        self.assertFalse(instance.phrase_is_generalization(pattern_phrase, other_phrase))

    def test_phrase_is_not_generalization_when_completely_different(self):
        instance = Generalizer(0.5)
        pattern_phrase = 'to be or not to be that is the question'.split(' ')
        other_phrase = 'to boldly go where no one has gone'.split(' ')
        self.assertFalse(instance.phrase_is_generalization(pattern_phrase, other_phrase))

    def test_phrase_is_not_generalization_with_no_slots(self):
        instance = Generalizer(0.5)
        pattern_phrase = 'to boldly go where no one has gone'.split(' ')
        other_phrase = 'to boldly go where no one has gone'.split(' ')
        self.assertFalse(instance.phrase_is_generalization(pattern_phrase, other_phrase))

    def test_phrase_is_not_generalization_when_over_abstraction_threshold(self):
        instance = Generalizer(0.5)
        pattern_phrase = 'to _ _ _ _ _ _ gone'.split(' ')
        other_phrase = 'to boldly go where no one has gone'.split(' ')
        self.assertFalse(instance.phrase_is_generalization(pattern_phrase, other_phrase))



if __name__ == '__main__':
    unittest.main()
