import argparse
import codecs
import glob
import json
import logging
import os
import sys

from docs_to_sentences import EXTENSION
from processors.process_document_step import ProcessDocumentStep
from processors.update_dictionary_step import UpdateDictionaryStep

LOGGER = logging.getLogger('dearing_single')
LOGGER.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
LOGGER.addHandler(handler)


def parse_directory_to_result_file(doc_filenames, out_filename):
    phrase_dictionary = {}
    for doc_filename in doc_filenames:
        with codecs.open(doc_filename, encoding='utf-8') as in_file:
            in_file_content = in_file.readlines()
            doc_processor = ProcessDocumentStep(phrase_dictionary, in_file_content, doc_filename, LOGGER)
            doc_processor.execute()
            update_messages = doc_processor.get_updates()
            dictionary_updater = UpdateDictionaryStep(phrase_dictionary, update_messages, LOGGER)
            dictionary_updater.execute()
    with open(out_filename, 'w') as out_file:
        results = clean_results(phrase_dictionary)
        json.dump(results, out_file)


def clean_results(phrase_dictionary):
    phrases = {}
    for _, phrase_results in phrase_dictionary.items():
        for phrase, sources in phrase_results.items():
            if len(sources) > 1:
                phrases[phrase] = list(sources)
    return phrases


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Convert text file to sentences')
    argparser.add_argument('in_path', type=str, help='Location of input files')
    argparser.add_argument('out_filename', type=str, help='File to write results to')
    args = argparser.parse_args()
    LOGGER.info('Starting Dearing ...')
    LOGGER.info('Input path %s and output filename %s', args.in_path, args.out_filename)
    doc_filenames = glob.glob(os.path.join(args.in_path, '*' + EXTENSION))
    parse_directory_to_result_file(doc_filenames, args.out_filename)
