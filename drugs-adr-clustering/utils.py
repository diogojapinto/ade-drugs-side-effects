"""
    Utility functions
"""

import numpy as np
import math as m
from constants import NORMAL_TRAINING_SET_SIZE

def get_training_and_test_sets(dataframe):
    """ Separates the training set (70%) and test set (30%) """
    dataframe = dataframe.reindex(np.random.permutation(dataframe.index))

    test_end = m.floor(len(dataframe) * NORMAL_TRAINING_SET_SIZE)

    return dataframe[:test_end], dataframe[test_end:]
