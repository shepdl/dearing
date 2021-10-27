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
            # I think really what we want to do is generalize phrases, so that
            # if a more general form of a phrase shows up, we want to link it back
            for word in message.phrase:
                if not word:
                    continue
                if word not in self._phrase_dictionary:
                    self._phrase_dictionary[word] = {}
                if phrase_string not in self._phrase_dictionary[word]:
                    self._phrase_dictionary[word][phrase_string] = set()
                self._phrase_dictionary[word][phrase_string].add(message.file_name)
        return self._phrase_dictionary
