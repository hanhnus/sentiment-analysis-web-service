"""
A function used for input text pre-processing
"""

import re
import logging
import unidecode
import string

from bs4            import BeautifulSoup
from nltk.corpus    import stopwords
from nltk.tokenize  import word_tokenize
# from pycontractions import Contractions


def text_preprocessing(text, lower_case         = True,
                             rm_num             = True,
                             rm_html_tags       = True,
                             rm_whitespaces     = True,
                             rm_punctuation     = True,
                             rm_stop_words      = True,
                             conv_accented_char = True):

    """
    Pre-process the input text

      lower_case          Boolean  to convert all the letters in the input text into lower case
      rm_num              Boolean  to remove all the digits in the input text
      rm_html_tags        Boolean  to remove all the HTML tags (<head>, <p>, etc) in the input text
      rm_whitespaces      Boolean  to remove all the whitespaces ("\t", "\n", "\r", etc)
                                   in the input text
      rm_punctuation      Boolean  to remove all the punctuation (!"#$%&'()*+, -./:;<=>?@[\]^_`{|}~)
                                   in the input text
      rm_stop_words       Boolean  to remove all the stop words ("the", "a", "on", "is", "all", etc,
                                   which usually do not carry important meaning) in the input text
      conv_accented_char  Boolean  to convert and standardize the input text (e.g. latté to latte,
                                   café to cafe)
    """

    acc_char_mapping = {}
    #logger.info("input_sentence: " + sentence)

    # convert text to lowercase
    if lower_case == True:
        text = text.lower()
        #logger.info("pre-proc lowercase:          " + sentence)

    # remove numbers if not relevant
    # r - string is to be treated as a raw string: all escape codes will be ignored.
    #     e.g. r'\n' will be treated as the characters \ followed by n.
    if rm_num == True:
        text = re.sub(r'\d+', '', text)
        #logger.info("pre-proc rm_num:             " + sentence)

    # remove HTML tags
    if rm_html_tags == True:
        soup     = BeautifulSoup(text, "html.parser")
        text = soup.get_text(separator =" ")
        #logger.info("pre-proc rm_html_tags:       " + sentence)

    # remove whitespaces
    if rm_whitespaces == True:
        text = text.strip()
        #logger.info("pre-proc rm_whitespaces:     " + sentence)

    # expand contractions
    # https://pypi.org/project/pycontractions/
    # if expand_contractions == True:
    # sentence = list(cont.expand_texts([sentence], precise = True))[0]

    # remove punctuation
    # str.maketrans(from_str, to_str, delete_str)
    if rm_punctuation == True:
        text = text.translate(str.maketrans("", "", string.punctuation))
        #logger.info("pre-proc rm_punctuation:     " + sentence)

    # remove stop words
    if rm_stop_words == True:
        stop_words  = set(stopwords.words('english'))
        list_tokens = word_tokenize(text)
        list_tokens = [words for words in list_tokens if not words in stop_words]
        text    = " ".join(list_tokens)
        #logger.info("pre-proc rm_stop_words:      " + sentence)

    # convert accented characters
    if conv_accented_char == True:
        text = unidecode.unidecode(text)
        # dummy mapping
        acc_char_mapping = {'è': 'e',
                            'é': 'e'}
        #logger.info("pre-proc conv_accented_char: " + sentence)

    #return sentence, acc_char_mapping
    return text