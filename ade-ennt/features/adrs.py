"""
    Builds a Drug-ADR matrix from ADReCS
"""

import pandas as pd
from ..utils import log
from ..libs.adrecs import get_drug_adr_matrix

ADRS_FILE = '../data/adrs.p'

def build_matrix():
    """ Loads or fetches the drug-adr matrix, as needed """
    try:
        matrix_df = pd.read_pickle(ADRS_FILE)

        log("Drug-ADR matrix loaded from local files")

    except FileNotFoundError:
        log('Fetching Drug-ADR matrix from database')

        matrix_df = get_drug_adr_matrix()

        # rename the indices (commented because there are a lot of names)
        #drugs = matrix_df.index.values.tolist()
        #adrs = matrix_df.columns.values.tolist()

        #matrix_df.rename(index=drug_names_dict, columns=adr_names_dict)

        matrix_df.to_pickle(ADRS_FILE, 'wb')

        log("Done and saved locally")

    return matrix_df


if __name__ == "__main__":
    print(build_matrix())
