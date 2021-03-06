"""
    Functionality related to running SVM
"""

import numpy as np
import pandas as pd
import random as rd

MV_RATIO = 0.3

def export_matrices_in_csv():
    """ Exports the original matrix and one with missing values to CSV files """

    matrix_df = pd.read_pickle('data/bipartite_df.p')
    matrix = matrix_df.as_matrix()
    matrix = matrix.astype(int)

    np.savetxt('data/original.csv', matrix, delimiter=',', fmt='%i')

    add_missing_values(matrix)

    np.savetxt('data/with-mv.csv', matrix, delimiter=',', fmt='%i')


def add_missing_values(matrix):
    """ Sets some true relations to false """

    for i in range(len(matrix)):
        mask = matrix[i] == 5

        for j in range(len(mask)):
            if mask[j] == False:
                continue

            sample = rd.random()
            if sample > MV_RATIO:
                mask[j] = False

        matrix[i, mask] = 0


if __name__ == '__main__':
    export_matrices_in_csv()
