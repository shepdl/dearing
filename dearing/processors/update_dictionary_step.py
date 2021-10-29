class DictionaryUpdateRequest:

    def __init__(self, phrase, file_name):
        self.phrase = phrase
        self.file_name = file_name

    def phrase_string(self):
        phrase = ' '.join([m or '_' for m in self.phrase])
        return phrase

    def is_generalization(self):
        return not all(self.phrase is not None)


class UpdateDictionaryStep:

    def __init__(self, phrase_dictionary, update_messages, logger, generalizer=None):
        self._phrase_dictionary = phrase_dictionary
        self._update_messages = update_messages
        self._logger = logger

        self._generalizer = generalizer or Generalizer(0.5, 2)

    def execute(self):
        self._logger.debug('Updating dictionary')
        for message in self._update_messages:
            phrase_string = message.phrase_string()
            # I think really what we want to do is generalize phrases, so that
            # if a more general form of a phrase shows up, we want to link it back
            for word in message.phrase:
                if not word:  # Skip spaces and Nones, obviously
                    continue
                if word not in self._phrase_dictionary:
                    self._phrase_dictionary[word] = {}
                if phrase_string not in self._phrase_dictionary[word]:
                    self._phrase_dictionary[word][phrase_string] = set()
                phrases_generalized = []
                for phrase in self._phrase_dictionary[word]:
                    if self._generalizer.phrase_is_generalization(message.phrase, phrase.split(' ')):
                        if phrase_string != phrase:
                            phrases_generalized.append(phrase)
                        self.merge_phrases(word, phrase_string, phrase)
                for phrase in phrases_generalized:
                    del self._phrase_dictionary[word][phrase]
                self._phrase_dictionary[word][phrase_string].add(message.file_name)
        return self._phrase_dictionary

    def merge_phrases(self, word, source_phrase, target_phrase):
        self._phrase_dictionary[word][source_phrase] = self._phrase_dictionary[word][source_phrase].union(
            self._phrase_dictionary[word][target_phrase]
        )


class Generalizer:

    def __init__(self, abstraction_threshold, length_difference_threshold=2):
        self._abstraction_threshold = abstraction_threshold
        self.length_difference_threshold = length_difference_threshold

    def phrase_is_generalization(self, pattern_phrase, other_phrase) -> bool:
        # phrases must be within 2 tokens
        if abs(len(pattern_phrase) - len(other_phrase)) > self.length_difference_threshold:
            return False
        # pattern_phrase must be at least 50% real words
        slot_count = len([t for t in pattern_phrase if t is None or t == '_'])
        if slot_count == 0 and pattern_phrase == other_phrase:
            return False
        if slot_count / len(pattern_phrase) > self._abstraction_threshold:
            return False
        # other_phrase must have words where pattern has slots
        for pattern_token, other_phrase_token in zip(pattern_phrase, other_phrase):
            if pattern_token is None or pattern_token == '_':
                continue
            if pattern_token != other_phrase_token:
                return False

        return True
