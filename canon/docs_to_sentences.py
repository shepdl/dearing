""" Convert a set of files into sentences and write them out to out_path """

import argparse
import glob
import os
import logging
import sys

EXTENSION = '.sents.txt'

LOGGER = logging.getLogger('docs-to-sentences')
LOGGER.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
LOGGER.addHandler(handler)


def main(in_path, out_path):
    """
    :param in_path: location of files
    :param out_path: location of out_files. The out files will be written there with the extension .sents.txt
    :return:
    """
    LOGGER.info('Loading model ...')
    import spacy
    nlp = spacy.load('en_core_web_md')
    LOGGER.info('Model loaded')
    sentencizer = nlp.add_pipe('sentencizer')
    for filename in glob.glob(in_path):
        with open(filename) as in_file:
            in_file_content = in_file.read()
        LOGGER.info('Parsing %s', filename)
        doc = nlp(in_file_content)
        in_basename = os.path.basename(filename)
        out_filename = os.path.join(out_path, in_basename.rsplit('.', 1)[0] + EXTENSION)
        with open(out_filename, 'w') as out_file:
            for sent in doc.sents:
                tokens_to_keep = [token.text for token in sent if not token.is_punct and not token.is_space]
                tokens_to_keep = [token.lower() for token in tokens_to_keep if '\n' not in token]
                out_file.write(' '.join(tokens_to_keep))
                out_file.write('\n')
        LOGGER.info('Wrote %s', filename)
    LOGGER.info('Done')


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Convert text file to sentences')
    argparser.add_argument('in_path', type=str, help='Location of input files')
    argparser.add_argument('out_path', type=str, help='Location to write files to')
    args = argparser.parse_args()
    main(args.in_path, args.out_path)