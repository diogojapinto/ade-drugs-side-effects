"""
    Module that retrieves, cleans and merges the molecular descriptors for drugs with the ADRs
"""

import pandas as pd
import numpy as np
from sklearn import preprocessing

def append_descriptors(drugs_df):
    """ First just some tests """

    # clean
    descriptors_df = pd.read_csv('data/drugs1_2d.csv', index_col="Name", na_values=['Infinity', ''])
    descriptors_df.dropna(axis=0, inplace=True)

    descriptors_df = descriptors_df.groupby(level=0).aggregate(np.mean)

    # scale everything
    values = descriptors_df.values
    drugs_names = descriptors_df.index.values
    descriptors_names = descriptors_df.columns.values

    min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0,5))
    scaled_values = min_max_scaler.fit_transform(values)
    descriptors_df = pd.DataFrame(scaled_values, index=drugs_names, columns=descriptors_names)

    # join
    result_df = drugs_df.join(descriptors_df, how='inner')


    return result_df