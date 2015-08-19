"""
    Builds a Drug-ADR matrix from ADReCS
"""

import pandas as pd
from utils import log
from libs.adrecs import get_drug_adr_matrix

def adrs_file(level):
    """ Returns the path to the adr file with the desired level """
    return '../data/adrs' + str(level) + '.p'

def generate(level=4):
    """ Loads or fetches the drug-adr matrix, as needed """

    try:
        matrix_df = pd.read_pickle(adrs_file(level))
        log("Drug-ADR matrix loaded from local files")

    except FileNotFoundError:
        log('Fetching Drug-ADR matrix from database')

        matrix_df = get_drug_adr_matrix(level)
        matrix_df.to_pickle(adrs_file(level), 'wb')
        
        log("Done and saved locally")

    return matrix_df


if __name__ == "__main__":
    print(generate())
