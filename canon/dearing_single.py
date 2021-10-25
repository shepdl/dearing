import argparse
import codecs
import collections
import glob
import logging
import os
import sys
import typing

from docs_to_sentences import EXTENSION

LOGGER = logging.getLogger('dearing_single')
LOGGER.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
LOGGER.addHandler(handler)


class ProcessDocumentStep:

    def __init__(self, phrase_dictionary, in_file_content, in_file_name, logger):
        self._phrases = phrase_dictionary
        self._content = in_file_content
        self._in_file_name = in_file_name
        self._logger = logger

        self._max_word_deviations_allowed = 5
        self._phrase_threshold = 4

        self._updates = []

    def execute(self):
        updates = []
        for sentence in self._content:
            sentence = sentence.strip()
            sentence_tokens = sentence.split(' ')
            seen_sentence_tokens = set()
            for sentence_index, sentence_token in enumerate(sentence_tokens):
                if not sentence_token or sentence_token in seen_sentence_tokens:
                    continue
                seen_sentence_tokens.add(sentence_token)
                if sentence_token in self._phrases:
                    for phrase in self._phrases[sentence_token]:
                        phrase_tokens = phrase.split(' ')
                        word_deviations = self._max_word_deviations_allowed
                        phrase_index = 0
                        token_sentence_index = sentence_index
                        matches = []
                        while phrase_index < len(phrase_tokens) and token_sentence_index < len(sentence_tokens) and word_deviations > 0:
                            if sentence_tokens[token_sentence_index] != phrase_tokens[phrase_index]:
                                word_deviations -= 1
                                matches.append(None)
                            else:
                                word_deviations = self._max_word_deviations_allowed
                                matches.append(phrase_tokens[phrase_index])
                            token_sentence_index += 1
                            phrase_index += 1

                        # Trim off Nones at end
                        matches.reverse()
                        matches = matches[matches.index(None):]
                        matches.reverse()
                        if len([m for m in matches if m is not None]) >= self._phrase_threshold:
                            # phrase = ' '.join([m or '_' for m in matches])
                            updates.append(DictionaryUpdateRequest(matches, self._phrases, self._in_file_name))
                            # new_phrases = self._phrases[sentence_token].copy()
                            # new_phrases.extend({phrase: self._in_file_name, })
                            # updates.append( ([sentence_token], new_phrases) )
                            # set updates: link common phrase to all the words in it, and all the dictionaries.
                            # move to next position after the phrase

                else:
                    updates.append(DictionaryUpdateRequest(sentence_tokens, self._phrases, self._in_file_name))
                    # updates.append( ([sentence_token], { sentence: self._in_file_name }) )
                    # updates.append( ([sentence_token], [], [sentence, self._in_file_name,],) )
        self._updates.extend(updates)

    def get_updates(self) -> typing.List[typing.Tuple]:
        return self._updates
        # Update structure:
        # ([words], [phrases], [(sentence, filename,),]


class DictionaryUpdateRequest:

    def __init__(self, phrase, original_phrase_dictionary, file_name):
        self.phrase = phrase
        self.phrase_dictionary = original_phrase_dictionary
        self.file_name = file_name

    def phrase_string(self):
        phrase = ' '.join([m or '_' for m in self.phrase])
        return phrase


class UpdateDictionaryStep:

    def __init__(self, phrase_dictionary, update_messages, logger):
        self._phrase_dictionary = phrase_dictionary
        self._update_messages = update_messages
        self._logger = logger

    def execute(self):
        self._logger.debug('Updating dictionary')
        for message in self._update_messages:
            phrase_string = message.phrase_string()
            for word in message.phrase:
                if not word:
                    continue
                if word not in self._phrase_dictionary:
                    self._phrase_dictionary[word] = {}
                if phrase_string not in self._phrase_dictionary[word]:
                    self._phrase_dictionary[word][phrase_string] = set()
                self._phrase_dictionary[word][phrase_string].add(message.file_name)
        return self._phrase_dictionary


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


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Convert text file to sentences')
    argparser.add_argument('in_path', type=str, help='Location of input files')
    argparser.add_argument('out_filename', type=str, help='File to write results to')
    args = argparser.parse_args()
    LOGGER.info('Starting Dearing ...')
    LOGGER.info('Input path %s and output filename %s', args.in_path, args.out_filename)
    doc_filenames = glob.glob(os.path.join(args.in_path, '*' + EXTENSION))
    parse_directory_to_result_file(doc_filenames, args.out_filename)
