"""
    Module that retrieves, cleans and merges the molecular descriptors for drugs with the ADRs
"""

import pandas as pd
import numpy as np
import adrecs_interface as ai
import pickle as pk

def append_descriptors(drugs_df):
    """ First just some tests """

    # clean
    descriptors_df = pd.read_csv('data/drugs1_2d.csv', index_col="Name", na_values=['Infinity', ''])
    descriptors_df.dropna(axis=0, inplace=True)

    descriptors_df = descriptors_df.groupby(level=0).aggregate(np.mean)

    # join
    result_df = drugs_df.join(descriptors_df, how='inner')


    return result_df