"""
    Module that retrieves, cleans and merges the molecular descriptors for drugs with the ADRs
"""

import pandas as pd
import numpy as np
import adrecs_interface as ai

def append():
    """ First just some tests """

    drugs_df = pd.read_pickle('data/bipartite_df.p')

    # rename the indices
    drugs = matrix_df.index.values.tolist()
    adrs = matrix_df.columns.values.tolist()

    drug_names_dict = {x: ai.get_drug_name(x) fro x in drugs}
    adr_names_dict = {x: ai.get_drug_name(x) fro x in drugs}
    drugs_df.rename(index=drug_names_dict, columns=adr_names_dict)

    descriptors_df = pd.read_csv('data/drugs1_2d.csv', index_col="Name", na_values=['Infinity', ''])
    descriptors_df.dropna(axis=0, inplace=True)

    descriptors_df['index'] = descriptors_df.index
    descriptors_df = descriptors_df.groupby('index').aggregate(np.mean)

    return drugs_df, descriptors_df
