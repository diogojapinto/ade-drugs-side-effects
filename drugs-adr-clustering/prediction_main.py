"""
	Uses the latent factors algorithm to predict new drugs adrs

	Elements: drugs
	Features: ADRs (next increment: main quemical structures)
"""

import pickle as pk
import adrecs_interface as ai
from utils import get_training_and_test_sets
from sys import argv
import latent_factors_utils as lf
import pandas
from constants import MAX_TO_KEEP, MIN_TO_KEEP, NR_ITERATIONS
import numpy as np
import scipy as sp
import datetime
import time
import pdb

def main():
    """ Entry function.
        When computation is too long, saves objects to files"""

    testing = False

    if len(argv) > 1 and argv[1] == 'test':
        print("Running in test mode")
        testing = True
    else:
        print("Running in normal mode")

    try:
        matrix_df = pk.load(open('data/bipartite_df.p', 'rb'))
    except FileNotFoundError:
        log('Fetching drug adr matrix')
        matrix_df = ai.get_drug_adr_matrix()
        pk.dump(matrix_df, open('data/bipartite_df.p', 'wb'))

    # get the training and test sets
    if testing:
        log('Dividing matrix in test and training sets')
        matrix_df, test_set = get_training_and_test_sets(matrix_df)

    # retrieve the numpy matrix, drugs names and adrs names
    matrix = matrix_df.as_matrix()
    drugs = matrix_df.index.values.tolist()
    adrs = matrix_df.columns.values.tolist()

    log('Computing SVD')
    # compute the svd
    u_mat, s_array, v_mat = lf.compute_svd(matrix)

    log('Reducing Singular Values')
    # remove the unuseful lines
    u_mat, s_array, v_mat = lf.reduce_singular_values(u_mat, s_array, v_mat)

    # log('Computing Root Mean Squared')
    # confirm the RMSE
    # preliminary_rmse = lf.compute_rmse(matrix, lf.reconstruct_matrix(u_mat, v_mat, s_array))
    # print("RMSE after reducing dimension: %f" % (preliminary_rmse))

    log('Applying gradient descent')
    # scale the matrixes and perform gradient desc«ent on it
    p_mat, q_mat = lf.get_scaled_matrices(u_mat, s_array, v_mat)
    # pdb.set_trace()
    p_mat, q_mat = lf.gradient_descent(matrix, p_mat, q_mat, testing)

    log('Testing...')
    # test things out
    if testing:
        test_latent_factors(q_mat, test_set)

    # Return the matrixes with the corresponding indexes
    p_df = pandas.DataFrame(p_mat, index=drugs)
    q_df = pandas.DataFrame(q_mat.transpose(), index=adrs)

    return p_df, q_df

def test_latent_factors(q_mat, test_set):
    """ Computes the average error of the obtained latent factors model
        based on the average root_mean_square error of the test_set """
    errors = []
    test_set = test_set.as_matrix()

    for _ in range(NR_ITERATIONS):
        line_i = np.random.randint(0, len(test_set))
        original_obj = test_set[line_i]
        obj = original_obj.copy


        # put some of them in 0
        zeroed_elems_ratio = (MAX_TO_KEEP - MIN_TO_KEEP) * np.random.random_sample() + MIN_TO_KEEP
        candidates = obj > 0

        for index, elem in enumerate(candidates):
            if elem == False:
                continue
            prob = np.random.random_sample()
            if prob <= zeroed_elems_ratio:
                obj[index] = 0

        obj_factors = obj.dot(q_mat.transpose())
        new_obj = obj_factors.dot(q_mat)

        errors.append(lf.compute_rmse(original_obj, new_obj))

    print("Mean : {0:8.6f}".format(sp.mean(errors)))
    print("Minimum : {0:8.6f}".format(min(errors)))
    print("Maximum : {0:8.6f}".format(max(errors)))
    print("Variance : {0:8.6f}".format(sp.var(errors)))
    print("Std. deviation : {0:8.6f}".format(sp.std(errors)))

def predict(q_mat, obj):
    return (obj.dot(q_mat.transpose())).dot(q_mat)

def log(message):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    print('[' + st + ']', message)

if __name__ == "__main__":
    main()


"""
funcoes a implementar:
    calcular distancia entre drugs (cosine distance entre drug * adr2concept)
    calcular distancia entre adrs (cosine distance entre adr * drug2concept)

    cluster de adrs (baseado no cosine distance dos concepts(k-means, k=no de adrs pode resolver isto))
    cluster de drugs (baseado no cosine distance dos concepts(k-means, k=no de drugs pode resolver isto))

    prever adrs de drugs (drug * adr2concept * adr2concept^T)
    prever drugs que tem uma dada adr (adr * drug2concept * drug2concept^T)
"""

def predict_adrs(drug, q_mat):
    pass