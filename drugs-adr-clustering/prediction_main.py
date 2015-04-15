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
    elif len(argv) > 1 and argv[1] == 'results':
        print('Testing results')
    else:
        print("Running in normal mode")

    try:
        matrix_df = pd.read_pickle('data/bipartite_df.p')
    except FileNotFoundError:
        log('Fetching drug adr matrix')
        matrix_df = ai.get_drug_adr_matrix()
        pk.dump(matrix_df, open('data/bipartite_df.p', 'wb'))

    # get the training and test sets
    if testing:
        try:
            matrix_df = pd.read_pickle('data/training_set.p')
            test_set = pd.read_pickle('data/test_set.p')
        except FileNotFoundError:
            log('Dividing matrix in test and training sets')
            matrix_df, test_set = get_training_and_test_sets(matrix_df)

    # retrieve the numpy matrix, drugs names and adrs names
    matrix = matrix_df.as_matrix()
    
    drugs = matrix_df.index.values.tolist()
    adrs = matrix_df.columns.values.tolist()

    max_area = 0
    kf=cross_validation.KFold(n=len(drugs), n_folds=10)
    for train_index, test_index in kf:
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

        area,_,_ =test.test_roc(q_mat, matrix_df.iloc[test_index,:])
        
        # Maximizing area. It might be best to try and maximize precision and recal
        if area > max_area:
            best_q_mat = q_mat
            max_area = area
            matrix_df.iloc[train_index,:].index.values.tolist()

    print("Best area =",max_area)
    log('Testing...')
    # test things out
    if testing:
        _, threshold, predictions = test.test_roc(best_q_mat, test_set)
        test.precisionRecall(predictions, threshold, test_set)

    return p_mat, q_mat

def save_mat():
    try:
        matrix_df = pd.read_pickle('data/training_set.p')
        test_set = pd.read_pickle('data/test_set.p')
    except FileNotFoundError:
        log('Dividing matrix in test and training sets')
        matrix_df, test_set = get_training_and_test_sets(matrix_df)

    matrix = matrix_df.as_matrix()
    spi.savemat('train_set.mat', {'matrix': matrix})

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
