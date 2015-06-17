"""
    Utilitary functions
"""

import time
import datetime
import pickle as pk
from libs.adrecs import get_drugs_name_to_id_dict
import numpy as np
import math as m
from config import NORMAL_TRAINING_SET_SIZE

DRUGS_CONVERTER_FILE = './data/drugs-converter.p'

def log(message):
    """ logs a given message, binding a timestamp """
    timestamp = time.time()
    time_string = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    print('[' + time_string + ']', message)


def convert_drug_name_to_id(drug_name):
    """ Converts a given drug name to the id used in ADReCS """

    try:
        drugs_dict = pk.load(open(DRUGS_CONVERTER_FILE, 'rb'))
    except FileNotFoundError:
        # fills the dictionary
        drugs_dict = get_drugs_name_to_id_dict()

        pk.dump(drugs_dict, open(DRUGS_CONVERTER_FILE, 'wb'))

    return drugs_dict[drug_name.lower()]
    

def get_training_and_test_sets(dataframe):
    """ Separates the training set (70%) and test set (30%) """
    dataframe = dataframe.reindex(np.random.permutation(dataframe.index))

    test_end = m.floor(len(dataframe) * NORMAL_TRAINING_SET_SIZE)

    return dataframe[:test_end], dataframe[test_end:]
