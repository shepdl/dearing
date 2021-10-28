import logging
import sys

LOGGER = logging.getLogger('dearing_single')
LOGGER.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
LOGGER.addHandler(handler)


class TestHelpers:

    def notImplemented(self):
        self.fail('Not implemented')


