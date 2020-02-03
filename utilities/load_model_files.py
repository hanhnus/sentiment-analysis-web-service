"""
A function used for loading model files (model, mappings, dictionaries, 1-hot encoders, version)
"""

import pickle


def load_model_files(filename, logger):

    model_files = pickle.load(open(filename, 'rb'))
    logger.info('pickle loaded, file name: ' + str(filename))

    return model_files