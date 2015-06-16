"""
    Extracts the usable molecular descriptors
"""

import pandas as pd
import numpy as np
from ..utils import convert_drug_name_to_id
from ..utils import log

DESCRIPTORS_FILE = '../data/descriptors.csv'
RAW_DESCRIPTORS_CSV = '../data/drugs1_2d.csv'


def generate():
    """ Loads or fetches the drug-descriptor matrix, as needed """

    try:
        matrix_df = pd.read_pickle(DESCRIPTORS_FILE)
        log("Drug-Descriptors matrix loaded from local files")

    except FileNotFoundError:

        # clean
        matrix_df = pd.read_csv('data/drugs1_2d.csv', index_col="Name", na_values=['Infinity', ''])
        matrix_df.dropna(axis=0, inplace=True)
    
        matrix_df = matrix_df.groupby(level=0).aggregate(np.mean)
    
        # adjust the drug's names to ids
        drugs_names = matrix_df.index.values
        drugs_renaming = {x: convert_drug_name_to_id(x) for x in drugs_names}
    
        matrix_df.rename(index=drugs_renaming, inplace=True)

        matrix_df.to_pickle(DESCRIPTORS_FILE, 'wb')

        log("Done and saved locally")

    return matrix_df


if __name__ == "__main__":
    print(generate())
