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
import scipy as sp
import pylab as pl
import datetime
import time
import random
from utils import get_training_and_test_sets
from sys import argv
from constants import MAX_TO_KEEP, MIN_TO_KEEP, NR_ITERATIONS
from sklearn.metrics import roc_curve, auc

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
            pk.dump(matrix_df, open('data/training_set.p', 'wb'))
            pk.dump(test_set, open('data/test_set.p', 'wb'))

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

    log('Applying gradient descent')
    # scale the matrixes and perform gradient desc«ent on it
    p_mat, q_mat = lf.get_scaled_matrices(u_mat, s_array, v_mat)
    
    p_mat, q_mat = lf.gradient_descent(matrix, p_mat, q_mat, testing, 200)

    # Normalize
    p_mat = p_mat.dot(np.linalg.inv(lf.get_s_matrix(np.sqrt(s_array))))
    q_mat = np.linalg.inv(lf.get_s_matrix(np.sqrt(s_array))).dot(q_mat)

    log('Testing...')
    # test things out
    if testing:
        #print("Before: ")
        #test_latent_factors(v_mat, test_set)
        #print("After: ")
        #test_latent_factors(q_mat, test_set)
        test_roc(q_mat, test_set)

    # Return the matrixes with the corresponding indexes
    p_df = pd.DataFrame(p_mat, index=drugs)
    q_df = pd.DataFrame(q_mat.transpose(), index=adrs)

    pk.dump([p_df, q_df, s_array], open("data/final_product.p", 'wb'))

    # tests a single drug, and prints info
    #test_single()

    return p_df, q_df

def test_latent_factors(q_mat, test_set):
    """ Computes the average error of the obtained latent factors model
        based on the average root_mean_square error of the test_set """
    errors = []
    nr_elems_retracted = []
    test_set = test_set.as_matrix()

    for _ in range(NR_ITERATIONS):
        nr_elems_retracted.append(0)
        line_i = np.random.randint(0, len(test_set))
        original_obj = test_set[line_i]
        obj = original_obj.copy()


        # put some of them in 0
        zeroed_elems_ratio = (MAX_TO_KEEP - MIN_TO_KEEP) * np.random.random_sample() + MIN_TO_KEEP
        candidates = obj > 0

        for index, elem in enumerate(candidates):
            if elem == False:
                continue
            prob = np.random.random_sample()
            if prob <= zeroed_elems_ratio:
                obj[index] = 0
                nr_elems_retracted[len(nr_elems_retracted) - 1] += 1

        obj_factors = obj.dot(q_mat.transpose())
        new_obj = obj_factors.dot(q_mat)

        errors.append(lf.compute_rmse(original_obj, new_obj))

    print("REMOVED OBJECTS COUNT")
    print("Mean : {0:8.6f}".format(sp.mean(nr_elems_retracted)))
    print("Minimum : {0:8.6f}".format(min(nr_elems_retracted)))
    print("Maximum : {0:8.6f}".format(max(nr_elems_retracted)))
    print("Variance : {0:8.6f}".format(sp.var(nr_elems_retracted)))
    print("Std. deviation : {0:8.6f}".format(sp.std(nr_elems_retracted)))

    print("ERRORS")
    print("Mean : {0:8.6f}".format(sp.mean(errors)))
    print("Minimum : {0:8.6f}".format(min(errors)))
    print("Maximum : {0:8.6f}".format(max(errors)))
    print("Variance : {0:8.6f}".format(sp.var(errors)))
    print("Std. deviation : {0:8.6f}".format(sp.std(errors)))

def test_single():
    """ Tests a single random drug, printing the dataframe """
    matrix_df = pd.read_pickle('data/test_set.p')
    _, q_mat, _ = pd.read_pickle('data/final_product.p')

    original_drug = matrix_df.ix[random.sample(matrix_df.index.tolist(), 1)]

    drug_name = original_drug.index.tolist()[0]

    print("Selected %s" % drug_name)

    original_drug = original_drug.as_matrix()[0]
    edited_drug = original_drug.copy()

    zeroed_elems_ratio = (MAX_TO_KEEP - MIN_TO_KEEP) * np.random.random_sample() + MIN_TO_KEEP
    candidates = edited_drug > 0

    for index, elem in enumerate(candidates):
        if elem == False:
            continue
        prob = np.random.random_sample()
        if prob <= zeroed_elems_ratio:
            edited_drug[index] = 0

    drug_factors = edited_drug.dot(q_mat)
    drug_prediction = drug_factors.dot(q_mat.transpose())

    print("Error: %f" % lf.compute_rmse(original_drug, drug_prediction))

    results_df = pd.DataFrame([original_drug, edited_drug, drug_prediction], 
                                  index=['original', 'test', 'prediction'])
    print(results_df)
    print(results_df.iloc[:, candidates])

    fpr, tpr, thresholds = roc_curve(original_drug, drug_prediction, pos_label = 5)
    roc_auc = auc(fpr,tpr)
    print("Area under the curve: %f" % roc_auc )

    # Plot ROC curve
    pl.clf()
    pl.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
    pl.plot([0, 1], [0, 1], 'k--')
    pl.xlim([0.0, 1.0])
    pl.ylim([0.0, 1.0])
    pl.xlabel('False Positive Rate')
    pl.ylabel('True Positive Rate')
    pl.title('Receiver operating characteristic example')
    pl.legend(loc="lower right")
    pl.savefig('data/roc/' + drug_name)
    pl.show()

def test_roc(q_mat, test_set):
    errors = []
    nr_elems_retracted = []

    drug_names = test_set.index.tolist()
    test_set = test_set.as_matrix()

    rows, cols = test_set.shape
    roc_areas = []

    for r in range(rows):

        original_obj = test_set[r]
        obj = original_obj.copy()

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
        drug_prediction = obj_factors.dot(q_mat)

        fpr, tpr, thresholds = roc_curve(original_obj, drug_prediction, pos_label = 5)
        roc_auc = auc(fpr,tpr)
        roc_areas.append(roc_auc)

        # Plot ROC curve
        pl.clf()
        pl.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
        pl.plot([0, 1], [0, 1], 'k--')
        pl.xlim([0.0, 1.0])
        pl.ylim([0.0, 1.0])
        pl.xlabel('False Positive Rate')
        pl.ylabel('True Positive Rate')
        pl.title('Receiver operating characteristic for %s' % drug_names[r])
        pl.legend(loc="lower right")
        pl.savefig('data/roc/' + drug_names[r])

    print("Min Roc Area= %f" % min(roc_areas))
    print("Max Roc Area= %f" % max(roc_areas))


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
