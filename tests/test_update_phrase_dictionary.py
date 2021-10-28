import logging
import unittest

from processors import UpdateDictionaryStep
from processors.update_dictionary_step import DictionaryUpdateRequest
from tests.helpers_for_tests import TestHelpers



class UpdatePhraseDictionaryTests(unittest.TestCase, TestHelpers):

    LOGGER = logging.getLogger()

    def test_initially_empty_phrase_dictionary_contains_all_phrases(self):
        initial = {}
        messages = [
            DictionaryUpdateRequest(message, 'test file') for message in [
                'to be or not to be that is the question'.split(' '),
                'to eat or not to eat what a silly question'.split(' '),
            ]
        ]
        instance = UpdateDictionaryStep(initial, messages, self.LOGGER)
        results = instance.execute()
        expected = {keyword: {
            'to be or not to be that is the question': {'test file'},
            'to eat or not to eat what a silly question': {'test file'},
        } for keyword in [
            'to', 'or', 'not', 'question',
        ]}
        expected.update({keyword: {
            'to be or not to be that is the question': {'test file'},
        } for keyword in [ 'be', 'that', 'is', 'the', ]})
        expected.update({keyword: {
            'to eat or not to eat what a silly question': {'test file'},
        } for keyword in [ 'eat', 'what', 'a', 'silly', ]})
        self.assertEqual(expected, results)

    def test_phrase_dictionary_updated_with_some_new_words_some_new_phrases_and_some_existing_phrases_contains_all(self):
        initial = {
            'to': {
                'to be or not to be that is the question': {'test file'},
                'to eat or not to eat what a silly question': {'test file'},
                'to drink but not to drink what a hard question': {'new file'},
            },
            'but': {'to drink but not to drink what a hard question': {'new file'}},
            'drink': {'to drink but not to drink what a hard question': {'new file'}},
            'or': {
                'to be or not to be that is the question': {'test file'},
                'to eat or not to eat what a silly question': {'test file'},
                'to drink but not to drink what a hard question': {'new file'},
            },
            'not': {
                'to be or not to be that is the question': {'test file'},
                'to eat or not to eat what a silly question': {'test file'},
                'to drink but not to drink what a hard question': {'new file'},
            },
            'question': {
                'to be or not to be that is the question': {'test file'},
                'to eat or not to eat what a silly question': {'test file'},
            },
            'be': {'to be or not to be that is the question': {'test file'}},
            'that': {'to be or not to be that is the question': {'test file'}},
            'is': {'to be or not to be that is the question': {'test file'}},
            'the': {'to be or not to be that is the question': {'test file'}},
            'eat': {'to eat or not to eat what a silly question': {'test file'}},
            'what': {
                'to eat or not to eat what a silly question': {'test file'},
                'to drink but not to drink what a hard question': {'new file'},
            },
            'a': {
                'to eat or not to eat what a silly question': {'test file'},
                'to drink but not to drink what a hard question': {'new file'},
            },
            'silly': {'to eat or not to eat what a silly question': {'test file'}},
            'hard': {
                'to drink but not to drink what a hard question': {'new file'},
            }
        }
        messages = [
            DictionaryUpdateRequest(message, 'new file') for message in [
                'to drink but not to drink what a hard question'.split(' '),
            ]
        ]
        expected = {
            'to': {
                'to be or not to be that is the question': {'test file'},
                'to eat or not to eat what a silly question': {'test file'},
                'to drink but not to drink what a hard question': {'new file'},
            },
            'but': {'to drink but not to drink what a hard question': {'new file'}},
            'drink': {'to drink but not to drink what a hard question': {'new file'}},
            'or': {
                 'to be or not to be that is the question': {'test file'},
                 'to eat or not to eat what a silly question': {'test file'},
                 'to drink but not to drink what a hard question': {'new file'},
             },
             'not': {
                 'to be or not to be that is the question': {'test file'},
                 'to eat or not to eat what a silly question': {'test file'},
                 'to drink but not to drink what a hard question': {'new file'},
             },
             'question': {
                 'to be or not to be that is the question': {'test file'},
                 'to eat or not to eat what a silly question': {'test file'},
                 'to drink but not to drink what a hard question': {'new file'},
             },
             'be': {'to be or not to be that is the question': {'test file'}},
             'that': {'to be or not to be that is the question': {'test file'}},
             'is': {'to be or not to be that is the question': {'test file'}},
             'the': {'to be or not to be that is the question': {'test file'}},
             'eat': {'to eat or not to eat what a silly question': {'test file'}},
             'what': {
                 'to eat or not to eat what a silly question': {'test file'},
                 'to drink but not to drink what a hard question': {'new file'},
             },
             'a': {
                 'to eat or not to eat what a silly question': {'test file'},
                 'to drink but not to drink what a hard question': {'new file'},
             },
             'silly': {'to eat or not to eat what a silly question': {'test file'}},
            'hard': {
                'to drink but not to drink what a hard question': {'new file'},
            }
        }
        instance = UpdateDictionaryStep(initial, messages, self.LOGGER)
        results = instance.execute()
        self.assertEqual(expected, results)

