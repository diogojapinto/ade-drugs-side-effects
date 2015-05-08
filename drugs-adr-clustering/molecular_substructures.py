"""
    Module that retrieves, cleans and merges the molecular descriptors for drugs with the ADRs
"""

import pandas as pd

def main():
    """ First just some tests """

    drugs_df = pd.read_pickle('data/bipartite_df.p')

    descriptors_df = pd.read_csv('data/drugs1_2d.csv', index_col="Name")

    print(drugs_df)

if __name__ == '__main__':
    main()

