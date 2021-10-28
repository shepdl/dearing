import unittest

from processors import UpdateDictionaryStep
from processors.process_document_step import ProcessDocumentConfig, ProcessDocumentStep
from tests.helpers_for_tests import TestHelpers


class TestProcessDocumentStep(unittest.TestCase, TestHelpers):

    PHRASE_THRESHOLD = 3

    # Test case: "To be or not to be"

    PHRASE_DICTIONARY = {
        'to': {'to be or not to be': {'hamlet'}},
        'be': {'to be or not to be': {'hamlet'}},
        'or': {'to be or not to be': {'hamlet'}},
        'not': {'to be or not to be': {'hamlet'}},
    }

    def test_find_complete_overlap(self):
        test_content = ['to be or not to be']
        test_file_name = 'new file'
        phrase_dictionary = self.PHRASE_DICTIONARY.copy()
        config = ProcessDocumentConfig(3, self.PHRASE_THRESHOLD, LOGGER)
        instance = ProcessDocumentStep(phrase_dictionary, test_content, test_file_name, config)
        instance.execute()
        updates = instance.get_updates()
        update_step = UpdateDictionaryStep(phrase_dictionary, updates, config.logger)
        update_step.execute()
        self.assertEqual({
            'to': {'to be or not to be': {'hamlet', 'new file'}},
            'be': {'to be or not to be': {'hamlet', 'new file'}},
            'or': {'to be or not to be': {'hamlet', 'new file'}},
            'not': {'to be or not to be': {'hamlet', 'new file'}},
        }, phrase_dictionary)

    def test_find_partial_overlap_above_threshold(self):
        test_content = ['to think or not to think']
        test_file_name = 'new file'
        phrase_dictionary = self.PHRASE_DICTIONARY.copy()
        config = ProcessDocumentConfig(4, self.PHRASE_THRESHOLD, LOGGER)
        instance = ProcessDocumentStep(phrase_dictionary, test_content, test_file_name, config)
        instance.execute()
        updates = instance.get_updates()
        update_step = UpdateDictionaryStep(phrase_dictionary, updates, config.logger)
        update_step.execute()
        self.assertEqual({
            'to': {'to _ or not to': {'hamlet', 'new file'}, 'to think or not to think': {'new file'}},
            'be': {'to be or not to be': {'hamlet', 'new file'},},
            'think': {'to think or not to think': {'new file'}},
            'or': {'to _ or not to': {'hamlet', 'new file'}, 'to think or not to think': {'new file'}},
            'not': {'to _ or not to': {'hamlet', 'new file'}, 'to think or not to think': {'new file'}},
        }, phrase_dictionary)

    def test_find_partial_overlap_at_threshold(self):
        test_content = ['to think or not whatever']
        test_file_name = 'new file'
        phrase_dictionary = self.PHRASE_DICTIONARY.copy()
        config = ProcessDocumentConfig(4, self.PHRASE_THRESHOLD, LOGGER)
        instance = ProcessDocumentStep(phrase_dictionary, test_content, test_file_name, config)
        instance.execute()
        updates = instance.get_updates()
        update_step = UpdateDictionaryStep(phrase_dictionary, updates, config.logger)
        update_step.execute()
        self.assertEqual({
            'to': {'to think or not': {'new file'}, 'to _ or not': {'hamlet', 'new file'}},
            'be': {'to be or not to be': {'hamlet', 'new file'}},
            'or': {'to think or not': {'new file'}, 'to _ or not': {'hamlet', 'new file'}},
            'not': {'to think or not': {'new file'}, 'to _ or not': {'hamlet', 'new file'}},
            'think': {'to think or not': {'new file'}},
            'whatever': {'to think or not whatever': {'new file'}}
        }, phrase_dictionary)

    def test_skip_partial_overlap_below_threshold(self):
        test_content = ['to think or not whatever']
        test_file_name = 'new file'
        phrase_dictionary = self.PHRASE_DICTIONARY.copy()
        config = ProcessDocumentConfig(9, 5, LOGGER)
        instance = ProcessDocumentStep(phrase_dictionary, test_content, test_file_name, config)
        instance.execute()
        updates = instance.get_updates()
        update_step = UpdateDictionaryStep(phrase_dictionary, updates, config.logger)
        update_step.execute()
        self.assertEqual({
            'to': {'to be or not to be': {'hamlet'}},
            'be': {'to be or not to be': {'hamlet'},},
            'or': {'to be or not to be': {'hamlet'},},
            'not': {'to be or not to be': {'hamlet'},},
        }, phrase_dictionary)

    def test_add_no_overlap_to_dictionary(self):
        test_content = ['eh whatever who knows']
        test_file_name = 'new file'
        phrase_dictionary = self.PHRASE_DICTIONARY.copy()
        config = ProcessDocumentConfig(3, self.PHRASE_THRESHOLD, LOGGER)
        instance = ProcessDocumentStep(phrase_dictionary, test_content, test_file_name, config)
        instance.execute()
        updates = instance.get_updates()
        update_step = UpdateDictionaryStep(phrase_dictionary, updates, config.logger)
        update_step.execute()
        self.assertEqual({
            'to': {'to be or not to be': {'hamlet',}},
            'be': {'to be or not to be': {'hamlet',}},
            'or': {'to be or not to be': {'hamlet',}},
            'not': {'to be or not to be': {'hamlet',}},
            'eh': {'eh whatever who knows': {'new file'}},
            'whatever': {'eh whatever who knows': {'new file'}},
            'who': {'eh whatever who knows': {'new file'}},
            'knows': {'eh whatever who knows': {'new file'}},
        }, phrase_dictionary)
