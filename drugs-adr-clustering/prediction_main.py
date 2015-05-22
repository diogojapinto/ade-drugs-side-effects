"""
	Uses the latent factors algorithm to predict new drugs adrs

	Elements: drugs
	Features: ADRs (next increment: main quemical structures)
"""

import pickle as pk
import adrecs_interface as ai
import latent_factors_utils as lf
import pandas as pd
import numpy as np
import scipy.io as spi
import test
import datetime
import time
from utils import get_training_and_test_sets
from sys import argv
from sklearn import cross_validation
import matplotlib.pyplot as plt
from operator import itemgetter
from descriptors_cleaner import append_descriptors

def main():
    """ Entry function.
        When computation is too long, saves objects to files"""

    testing = False

    if len(argv) > 1 and argv[1] == 'test':
        print("Running in test mode")
        testing = True
    elif len(argv) > 1 and argv[1] == 'save':
        print('Saving mat')
        save_mat()
        return
    elif len(argv) > 1 and argv[1] == 'results':
        print('Testing results')
        test_results()
        return
    else:
        print("Running in normal mode")

    matrix_df = get_drug_adr_matrix()
    drugs = matrix_df.index.values.tolist()
    adrs = matrix_df.columns.values.tolist()

    # append descriptors
    matrix_df = append_descriptors(matrix_df)

    # get the training and test sets
    matrix_df, test_set = train_and_test_set(matrix_df)

    # retrieve the numpy matrix
    matrix = matrix_df.as_matrix()

    max_area = 0
    recall_area = []
    k_fold_nr = cross_validation.KFold(n=len(drugs), n_folds=10)
    for train_index, test_index in k_fold_nr:
        log('Computing SVD')
        # compute the svd
        u_mat, s_array, v_mat = lf.compute_svd(matrix_df.iloc[train_index,:])

        log('Reducing Singular Values')
        # remove the unuseful lines
        u_mat, s_array, v_mat = lf.reduce_singular_values(u_mat, s_array, v_mat)

        log('Applying gradient descent')
        # scale the matrixes and perform gradient desc«ent on it
        p_mat, q_mat = lf.get_scaled_matrices(u_mat, s_array, v_mat)
        p_mat, q_mat = lf.gradient_descent(matrix_df.iloc[train_index,:].as_matrix(), p_mat, q_mat, testing, 200)

        # Normalize
        p_mat = p_mat.dot(np.linalg.inv(lf.get_s_matrix(np.sqrt(s_array))))
        q_mat = np.linalg.inv(lf.get_s_matrix(np.sqrt(s_array))).dot(q_mat)

        area, threshold, predictions =test.test_roc(q_mat, matrix_df.iloc[test_index,:])

        # Save tuples for correlating area and recall
        _, recall = test.precision_recall(predictions, threshold, test_set) # LOOK HERE FOR test_set
        recall_area.append((recall, area))

        # Maximizing area. It might be best to try and maximize precision and recal
        if area > max_area:
            best_q_mat = q_mat
            max_area = area
            matrix_df.iloc[train_index,:].index.values.tolist()


    # tmp
    plt.plot(map(itemgetter(0), recall_area))
    plt.plot(map(itemgetter(1), recall_area))
    plt.show()
    plt.savefig("labels_and_colors.png")

    print("Best area =",max_area)
    log('Testing...')
    # test things out
    if testing:
        _, threshold, predictions = test.test_roc(best_q_mat, test_set)
        test.precision_recall(predictions, threshold, test_set)

    return p_mat, q_mat

def get_drug_adr_matrix():
    try:
        matrix_df = pd.read_pickle('data/bipartite_df.p')
    except FileNotFoundError:
        log('Fetching drug adr matrix')
        matrix_df = ai.get_drug_adr_matrix()

        # rename the indices
        drugs = matrix_df.index.values.tolist()
        adrs = matrix_df.columns.values.tolist()

        drug_names_dict = {x: ai.get_drug_name(x) for x in drugs}
        adr_names_dict = {x: ai.get_adr_name(x) for x in adrs}
        matrix_df.rename(index=drug_names_dict, columns=adr_names_dict)

        pk.dump(matrix_df, open('data/bipartite_df.p', 'wb'))

    return matrix_df

def train_and_test_set(matrix_df):
    try:
        train_set = pd.read_pickle('data/training_set.p')
        test_set = pd.read_pickle('data/test_set.p')
    except FileNotFoundError:
        log('Dividing matrix in test and training sets')
        train_set, test_set = get_training_and_test_sets(matrix_df)
        # Save test_set so it won't compromise future tests while using RMF
        pk.dump(test_set, open('data/test_set.p', 'wb'))

    return train_set, test_set

def save_mat():
    """ Saves training set in matlab format """

    # Fetch training set
    matrix_df = drug_adr_matrix()
    train_set, _ = train_and_test_set(matrix_df)

    # Save in a matlab readable format
    matrix = train_set.as_matrix()
    spi.savemat('data/train_set.mat', {'matrix': matrix})

def test_results():
    """ Reads matlab factorized matrix and tests it """

    # Fetch test set
    matrix_df = drug_adr_matrix()
    _, test_set = train_and_test_set(matrix_df)

    # Load matlab results
    mat_contents = spi.loadmat('data/results.mat')
    q_mat = mat_contents['q']

    # Test the solution and print it to the user
    _, threshold, predictions = test.test_roc(q_mat, test_set)
    test.precision_recall(predictions, threshold, test_set)


def predict_adrs(q_mat, obj):
    """ predicts the adrs for a given drug """
    return (obj.dot(q_mat.transpose())).dot(q_mat)

def log(message):
    """ logs a given message, binding a timestamp """
    timestamp = time.time()
    time_string = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    print('[' + time_string + ']', message)

if __name__ == "__main__":
    main()


"""
funcoes a implementar:
    calcular distancia entre drugs (cosine distance entre drug * adr2concept)
    calcular distancia entre adrs (cosine distance entre adr * drug2concept)

    cluster de adrs (baseado no cosine distance dos concepts(k-means, k=no de adrs pode resolver isto))
    cluster de drugs (baseado no cosine distance dos concepts(k-means, k=no de drugs pode resolver isto))
    --> caracterizar os clusters

    prever adrs de drugs (drug * adr2concept * adr2concept^T)
    prever drugs que tem uma dada adr (adr * drug2concept * drug2concept^T)

    droga mais relevante num cluster
    adr mais relevante num cluster


    (para clustering deve ser melhor descer o threshlold do reduce_singular_values)

    tirar adrs separados no tempo
"""
