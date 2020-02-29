"""
A function used for input text pre-processing
"""

import re
import logging
import unidecode
import string

import pandas as pd

from bs4            import BeautifulSoup
from nltk.corpus    import stopwords
from nltk.tokenize  import word_tokenize
# from pycontractions import Contractions


import sys
from nltk.sentiment.vader         import SentimentIntensityAnalyzer
from sklearn.linear_model         import LogisticRegression
from sklearn.pipeline             import Pipeline



def text_preprocessing(text,
                       f_lower_case         = True,
                       f_rm_num             = True,
                       f_rm_html_tags       = True,
                       f_rm_whitespaces     = True,
                       f_rm_punctuation     = True,
                       f_rm_stop_words      = True,
                       f_conv_accented_char = True):

    """
    Pre-process the input text

      f_lower_case          Boolean  to convert all the letters in the input text into lower case
      f_rm_num              Boolean  to remove all the digits in the input text
      f_rm_html_tags        Boolean  to remove all the HTML tags (<head>, <p>, etc) in the input text
      f_rm_whitespaces      Boolean  to remove all the whitespaces ("\t", "\n", "\r", etc)
                                     in the input text
      f_rm_punctuation      Boolean  to remove all the punctuation (!"#$%&'()*+, -./:;<=>?@[\]^_`{|}~)
                                     in the input text
      f_rm_stop_words       Boolean  to remove all the stop words ("the", "a", "on", "is", "all", etc,
                                     which usually do not carry important meaning) in the input text
      f_conv_accented_char  Boolean  to convert and standardize the input text (e.g. latté to latte,
                                     café to cafe)
    """

    acc_char_mapping = {}
    #logger.info("input_sentence: " + sentence)

    # convert text to lowercase
    if f_lower_case == True:
        text = text.lower()
        #logger.info("pre-proc lowercase:          " + sentence)

    # remove numbers if not relevant
    # r - string is to be treated as a raw string: all escape codes will be ignored.
    #     e.g. r'\n' will be treated as the characters \ followed by n.
    if f_rm_num == True:
        text = re.sub(r'\d+', '', text)
        #logger.info("pre-proc rm_num:             " + sentence)

    # remove HTML tags
    if f_rm_html_tags == True:
        soup     = BeautifulSoup(text, "html.parser")
        text = soup.get_text(separator =" ")
        #logger.info("pre-proc rm_html_tags:       " + sentence)

    # remove whitespaces
    if f_rm_whitespaces == True:
        text = text.strip()
        #logger.info("pre-proc rm_whitespaces:     " + sentence)

    # expand contractions
    # https://pypi.org/project/pycontractions/
    # if expand_contractions == True:
    # sentence = list(cont.expand_texts([sentence], precise = True))[0]

    # remove punctuation
    # str.maketrans(from_str, to_str, delete_str)
    if f_rm_punctuation == True:
        text = text.translate(str.maketrans("", "", string.punctuation))
        #logger.info("pre-proc rm_punctuation:     " + sentence)

    # remove stop words
    if f_rm_stop_words == True:
        stop_words  = set(stopwords.words('english'))
        list_tokens = word_tokenize(text)
        list_tokens = [words for words in list_tokens if not words in stop_words]
        text    = " ".join(list_tokens)
        #logger.info("pre-proc rm_stop_words:      " + sentence)

    # convert accented characters
    if f_conv_accented_char == True:
        text = unidecode.unidecode(text)
        # dummy mapping
        acc_char_mapping = {'è': 'e',
                            'é': 'e'}
        #logger.info("pre-proc conv_accented_char: " + sentence)

    #return sentence, acc_char_mapping
    return text




def df_preprocessing(list_text_files,
                     f_lower_case,
                     f_rm_num,
                     f_rm_html_tags,
                     f_rm_whitespaces,
                     f_rm_punctuation,
                     f_rm_stop_words,
                     f_conv_accented_char):

    list_df = []

    for text_file in list_text_files:
        # read data from file
        df = pd.read_csv(text_file,
                               sep    = '\t',
                               header = None,
                               names  = ['truth', 'text'])

        # pre-processing
        # training set will have 2 cols: text & truth after the pre-processing
        df['truth'] = df['truth'].str.replace('__label__', '').astype(int).astype('category')
        df['text'] = df['text'].apply(lambda x: text_preprocessing(x,
                                                                   f_lower_case,
                                                                   f_rm_num,
                                                                   f_rm_html_tags,
                                                                   f_rm_whitespaces,
                                                                   f_rm_punctuation,
                                                                   f_rm_stop_words,
                                                                   f_conv_accented_char))
        list_df.append(df)

    return list_df[0], list_df[1], list_df[2]



sys.path.append('..')
from train import f_lower_case, f_rm_num, f_rm_html_tags, f_rm_whitespaces, f_rm_punctuation, f_rm_stop_words, f_conv_accented_char


"""
A function called by api & HTML form endpoints for prediction
"""
def text_predict(text, model):

    dict_score = None

    if type(model) is SentimentIntensityAnalyzer:

        # text pre-processing
        text = text_preprocessing(text,
                                  f_lower_case= f_lower_case,
                                  f_rm_num= f_rm_num,
                                  f_rm_html_tags= f_rm_html_tags,
                                  f_rm_whitespaces= f_rm_whitespaces,
                                  f_rm_punctuation= f_rm_punctuation,
                                  f_rm_stop_words= f_rm_stop_words,
                                  f_conv_accented_char= f_conv_accented_char)

        # return floats for sentiment strength based on the input sentence
        dict_score = model.polarity_scores(text)

    elif type(model) is Pipeline and type(model['clf']) is LogisticRegression:

        # text pre-processing
        text = text_preprocessing(text,
                                  f_lower_case= f_lower_case,
                                  f_rm_num= f_rm_num,
                                  f_rm_html_tags= f_rm_html_tags,
                                  f_rm_whitespaces= f_rm_whitespaces,
                                  f_rm_punctuation= f_rm_punctuation,
                                  f_rm_stop_words= f_rm_stop_words,
                                  f_conv_accented_char= f_conv_accented_char)

        # return an int from 1-5
        dict_score = {'score': str(model.predict([text])[0])}
        print('LR Score: ' + str(dict_score) + '. ' + str(text))

    return dict_score