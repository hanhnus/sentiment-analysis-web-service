"""
A function called by api & HTML form endpoints for prediction
"""

import sys

sys.path.append('..')
from nltk.sentiment.vader         import SentimentIntensityAnalyzer
from sklearn.linear_model         import LogisticRegression
from sklearn.pipeline             import Pipeline
from utilities.text_preprocessing import text_preprocessing
from train                        import f_lower_case, f_rm_num, f_rm_html_tags, f_rm_whitespaces, f_rm_punctuation, f_rm_stop_words, f_conv_accented_char


def text_predict(text, model):

    dict_score = None

    if type(model) is SentimentIntensityAnalyzer:

        # text pre-processing
        text = text_preprocessing(text,
                                  lower_case         = f_lower_case,
                                  rm_num             = f_rm_num,
                                  rm_html_tags       = f_rm_html_tags,
                                  rm_whitespaces     = f_rm_whitespaces,
                                  rm_punctuation     = f_rm_punctuation,
                                  rm_stop_words      = f_rm_stop_words,
                                  conv_accented_char = f_conv_accented_char)

        # return floats for sentiment strength based on the input sentence
        dict_score = model.polarity_scores(text)

    elif type(model) is Pipeline and type(model['clf']) is LogisticRegression:

        # text pre-processing
        text = text_preprocessing(text,
                                  lower_case         = f_lower_case,
                                  rm_num             = f_rm_num,
                                  rm_html_tags       = f_rm_html_tags,
                                  rm_whitespaces     = f_rm_whitespaces,
                                  rm_punctuation     = f_rm_punctuation,
                                  rm_stop_words      = f_rm_stop_words,
                                  conv_accented_char = f_conv_accented_char)

        # return an int from 1-5
        dict_score = {'score': str(model.predict([text])[0])}
        print('LR Score: ' + str(dict_score) + '. ' + str(text))

    return dict_score