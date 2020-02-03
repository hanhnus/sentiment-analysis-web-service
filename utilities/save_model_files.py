"""
A function used for saving model files (model, mappings, dictionaries, 1-hot encoders, version)
used for pre-processing or transformation
"""

import pickle
import sys

from time import localtime, strftime


def save_model_files(filename, model, model_type, model_name, model_version, train_pred, logger):

    """
    save debugging info
      filename       str    file name to save in project folder
      model                 if train_pred is "train", model trained
                            if train_pred is "pred",  model used for prediction
      model_type     class  type(model)
      model_name     str    user-defined model name
      model_version  str    model trained/used local time
      train_pred     str    "train" - saved after training
                            "pred"  - saved when predicting
    """

    # model file preparing
    model_files = {'model':      model,
                   'model_type': model_type,
                   'model_name': model_name,
                   'version':    model_version,
                   'train/pred': train_pred}
    logger.info('model files saving:       ' + str(model_files))

    # save 2 model files; one with time, one without
    current_time       = strftime('%Y-%m-%d_%H-%M-%S', localtime())
    filename_with_time = filename + "_@" + str(current_time)
    pickle.dump(model_files, open(filename_with_time, 'wb'))
    logger.info('pickle dumped, file name: ' + str(filename_with_time))

    pickle.dump(model_files, open(filename, 'wb'))
    logger.info('pickle dumped, file name: ' + str(filename))
