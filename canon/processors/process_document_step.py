import typing

from processors.update_dictionary_step import DictionaryUpdateRequest


class ProcessDocumentConfig:

    def __init__(self, max_word_deviations, phrase_threshold, logger):
        self.max_word_deviations = max_word_deviations
        self.phrase_threshold = phrase_threshold
        self.logger = logger


class ProcessDocumentStep:

    def __init__(self, phrase_dictionary, in_file_content, in_file_name, config):
        self._phrases = phrase_dictionary
        self._content = in_file_content
        self._in_file_name = in_file_name
        self._logger = config.logger

        self._max_word_deviations_allowed = config.max_word_deviations
        self._phrase_threshold = config.phrase_threshold

        self._updates = []

    def get_updates(self) -> typing.List[typing.Tuple]:
        return self._updates

    def execute(self):
        updates = []
        for sentence in self._content:
            sentence = sentence.strip()
            sentence_tokens = sentence.split(' ')
            seen_sentence_tokens = set()
            sentence_index = 0
            while sentence_index < len(sentence_tokens) - self._phrase_threshold:
                # for sentence_index, sentence_token in enumerate(sentence_tokens):
                sentence_token = sentence_tokens[sentence_index]
                if not sentence_token or sentence_token in seen_sentence_tokens:
                    continue
                seen_sentence_tokens.add(sentence_token)
                if sentence_token in self._phrases:
                    longest_match = 0
                    for phrase in self._phrases[sentence_token]:
                        phrase_tokens = phrase.split(' ')
                        matches = self.longest_overlap(sentence_tokens[sentence_index:], phrase_tokens)
                        if self.is_long_enough(matches, self._phrase_threshold):
                            updates.append(DictionaryUpdateRequest(matches, self._phrases, self._in_file_name))
                            longest_match = max(len(matches), longest_match)
                            # TODO: update to include original sources of phrases
                            if None in matches:
                                another_match = sentence_tokens[sentence_index:sentence_index + len(matches) + 1]
                                updates.append(DictionaryUpdateRequest(another_match, self._phrases, self._in_file_name))
                    self._logger.info('Jumping ahead by %s', longest_match)
                    sentence_index += longest_match
                else:
                    self._logger.info('Did not find match; adding "%s"', ' '.join(sentence_tokens))
                    updates.append(DictionaryUpdateRequest(sentence_tokens, self._phrases, self._in_file_name))
                sentence_index += 1
        self._updates.extend(updates)

    @staticmethod
    def longest_overlap(sentence_tokens, phrase_tokens:typing.List[str], max_word_deviations_allowed=5):
        sentence_tokens = [token for token in sentence_tokens if token]
        word_deviations = max_word_deviations_allowed
        phrase_index = 0
        token_sentence_index = 0
        matches = []
        while phrase_index < len(phrase_tokens) and token_sentence_index < len(sentence_tokens) and word_deviations > 0:
            if sentence_tokens[token_sentence_index] == phrase_tokens[phrase_index]:
                word_deviations = max_word_deviations_allowed
                matches.append(phrase_tokens[phrase_index])
            else:
                word_deviations -= 1
                matches.append(None)
            token_sentence_index += 1
            phrase_index += 1

        # Trim off Nones at end
        counter = len(matches)
        while counter > 0:
            counter -= 1
            if matches[counter] is not None:
                break
        matches = matches[0:counter + 1]
        return matches

    @staticmethod
    def is_long_enough(phrase_tokens, phrase_threshold):
        return len([m for m in phrase_tokens if m is not None]) >= phrase_threshold
