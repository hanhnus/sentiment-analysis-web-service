"""
A training set called "sst_train.txt" needs to be provided to train a model.
Otherwise, the pre-built SentimentIntensityAnalyzer model will be output to
be loaded and run by app.py for production.

class Base, class VaderSentimentAnalyser & class LogisticRegressor
are resourced and modified from https://gist.github.com/prrao87
"""

import pytreebank
import sys
import os
import logging
import pandas as pd


from time                            import localtime, strftime
from nltk.sentiment.vader            import SentimentIntensityAnalyzer
from sklearn.metrics                 import accuracy_score, f1_score
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model            import LogisticRegression
from sklearn.pipeline                import Pipeline
from utilities.text_preprocessing    import text_preprocessing
from utilities.save_model_files      import save_model_files

# Logging setting
logging.basicConfig(level  = logging.INFO,
                    format = "%(asctime)s  %(levelname)8s  %(filename)12s  %(funcName)12s  %(lineno)4d  %(message)s")
training_logger = logging.getLogger("training_logger")


"""
Transform the Stanford Sentiment Treebank Dataset to Table Format

    The tree structure of phrases is converted to raw text and its associated class label
using the pytreebank library.

https://gist.github.com/prrao87/075a1160922ac21c47338bed59f70329#file-tree2tabular-py

After the transformation:

       instances  percentage
train       8544       72.1%
dev         1101        9.3%
test        2210       18.6%
"""

# out_path = os.path.join(sys.path[0], 'sst_{}.txt')
# dataset  = pytreebank.load_sst('./raw_data')
#
# # store train, dev and test in separate files
# for category in ['train', 'test', 'dev']:
#     with open(out_path.format(category), 'w') as outfile:
#         for item in dataset[category]:
#             outfile.write("__label__{}\t{}\n".format(
#                 item.to_labeled_lines()[0][0] + 1,
#                 item.to_labeled_lines()[0][1]
#             ))


class Base:
    """
    Base class
        houses common utilities for reading in test data
    and calculating model accuracy and F1 scores.
    """
    def __init__(self) -> None:
        pass

    def read_data(self,
                  file_name:          str,
                  lower_case:         bool = False,
                  rm_num:             bool = False,
                  rm_html_tags:       bool = False,
                  rm_whitespaces:     bool = False,
                  rm_punctuation:     bool = False,
                  rm_stop_words:      bool = False,
                  conv_accented_char: bool = False,
                  col_names = ['truth', 'text']) -> pd.DataFrame:
        """
        to read dataset, and pre-process the text in it (optional).
        """

        df = pd.read_csv(file_name,
                         sep    = '\t',
                         header = None,
                         names  = col_names)

        # categorise the truth labels
        df['truth'] = df['truth'].str.replace('__label__', '')
        df['truth'] = df['truth'].astype(int).astype('category')

        # pre-process the text data
        df['text'] = df['text'].apply(
            lambda x: text_preprocessing(x, lower_case,
                                            rm_num,
                                            rm_html_tags,
                                            rm_whitespaces,
                                            rm_punctuation,
                                            rm_stop_words,
                                            conv_accented_char))

        return df

    def print_performance(self, df: pd.DataFrame) -> None:
        """
        to calculate accuracy and F1 score
        """
        acc = accuracy_score(df['truth'], df['pred'])

        f1  = f1_score(df['truth'],
                       df['pred'],
                       average = 'macro')

        print("Accuracy:       {}\nMacro F1 score: {}".format(acc, f1))


class VaderSentimentAnalyser(Base):
    """
    VaderSentimentAnalyser class
        predicts sentiment scores (1-5) using Vader Sentiment Intensity Analyzer.
    """

    def __init__(self, model_file: str = None) -> None:
        super().__init__()
        self.vader_sia = SentimentIntensityAnalyzer()

    def score(self, text: str) -> float:
        """
        VADER breaks down sentiment intensity scores into a positive, negative and neutral component,
        which are then normalized and squashed to be within the range [-1, 1] as a “compound” score.
        """
        return self.vader_sia.polarity_scores(text)['compound']

    def predict_file(self, file: str) -> pd.DataFrame:
        """
        to predict class labels for instances in a file, usually the test set
        """
        df          = self.read_data(file)
        df['score'] = df['text'].apply(self.score)
        # convert float score to category based on binning
        print(df['pred'])
        df['pred']  = pd.cut(df['score'],
                             bins   = 5,
                             labels = [1, 2, 3, 4, 5])
        df = df.drop('score', axis = 1)

        return df


class LogisticRegressor(Base):
    """
    LogisticRegressor class
        predicts sentiment scores (1-5) using a sklearn Logistic Regression pipeline.
    """
    def __init__(self, model_file: str=None) -> None:
        """
        builds a pipeline to:
        1.
        2.
        3.
        """
        super().__init__()
        #self.regressor = LogisticRegression()
        self.regressor = None
        self.pipeline  = Pipeline(
            [
                ('vect',  CountVectorizer()),
                ('tfidf', TfidfTransformer()),
                ('clf',   LogisticRegression(solver      = 'liblinear',
                                             multi_class = 'auto')),
            ]
        )

    def train(self, train_file: str) -> pd.DataFrame:
        """
        to train a regressor using training set
        """
        df_train       = self.read_data(train_file)
        self.regressor = self.pipeline.fit(df_train['text'], df_train['truth'])['clf']
        #return self.regressor

    def predict(self, text: str) -> int:
        return self.pipeline.predict([text])[0]


    def predict_file(self, test_file:  str) -> pd.DataFrame:
        """
        to predict class labels in test set
        """
        df_test         = self.read_data(test_file)
        df_test['pred'] = self.pipeline.predict(df_test['text'])

        return df_test


# initialize the model
model = None

# training set in .txt format
training_text_file = 'sst_train.txt'

# Text pre-processing setting
f_lower_case         = False
f_rm_num             = False
f_rm_html_tags       = False
f_rm_whitespaces     = False
f_rm_punctuation     = False
f_rm_stop_words      = False
f_conv_accented_char = False

if os.path.exists(training_text_file):

    # read train data
    df_train = pd.read_csv(training_text_file,
                           sep    = '\t',
                           header = None,
                           names  = ['truth', 'text'])
    training_logger.info('training set loaded.')

    # pre-processing
    # training set will have 2 cols: text & truth after the pre-processing
    df_train['truth'] = df_train['truth'].str.replace('__label__', '')
    df_train['truth'] = df_train['truth'].astype(int).astype('category')
    df_train['text']  = df_train['text'].apply(lambda x: text_preprocessing(x,
                                                                            f_lower_case,
                                                                            f_rm_num,
                                                                            f_rm_html_tags,
                                                                            f_rm_whitespaces,
                                                                            f_rm_punctuation,
                                                                            f_rm_stop_words,
                                                                            f_conv_accented_char))
    training_logger.info('training set pre-processing done')
    print(df_train.head())

    #print("@test VaderSentimentAnalyser")
    #print(VaderSentimentAnalyser(Base).score("This is the best idea I've heard in a long time!"))
    #print(VaderSentimentAnalyser(Base).score("This is the worst idea I've heard!"))
    #print("@test VaderSentimentAnalyser")

    # train a Logistic Regression model
    logistic_regressor = LogisticRegressor(Base)
    logistic_regressor.train(training_text_file)
    training_logger.info('logistic_regressor trained')

    # predict on test set; after prediction, test set will have with 3 cols: text, truth, pred
    df_test = logistic_regressor.predict_file(training_text_file)
    print(df_test)
    training_logger.info('prediction done by logistic_regressor')

    # to calculate & print the accuracy & F1 score on test set
    print("Logistic Regression model performance:")
    logistic_regressor.print_performance(df_test)

    # to save the pipeline as model
    model = logistic_regressor.pipeline

else:
    """
    load Vader sentiment model is no training text file provided
    """
    model = SentimentIntensityAnalyzer()
    training_logger.info('model: ' + str(model))


# save model files to disk for app.py to load
save_model_files('sentiment_model_pickle',                     # filename
                 model,                                        # model
                 type(model),                                  # model_type
                 'sentiment-analysis',                         # model_name
                 str(strftime('%Y%m%d-%H%M%S', localtime())),  # model_version
                 'train',                                      # train_pred
                 training_logger)                              # logger, not for saving


