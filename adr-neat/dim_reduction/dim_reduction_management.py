"""
    Manages the dimensionality reduction of features
"""
from dim_reduction import svd
import pandas as pd
from features.features_management import get_feature

ALGORITHMS = {
    'svd': compute_svd,
    'rbm': compute_rbm,
    'pca': compute_pca
}

def get_dim_feature(ftr, alg):
    """ Returns the required feature after applying the required algorithm """

    return ALGORITHMS[alg](get_feature(ftr))


def get_dim_features(ftr_alg_pairs):
    """ Returns the required features after applying the required algorithms """

    # performs the first iteration, to initialize the array
    ftr0, alg0 = ftr_alg_pairs[0]
    result_df = get_dim_feature(ftr0, alg0)


    for ftr, alg in ftr_alg_pairs[1:]:
        result_df = result_df.join(get_dim_feature(ftr, alg), how='inner')

    return result_df


def compute_svd(matrix_df):
    """ Returns an indexed matrix, with the Singular-Value-Decomposition computed """
    drugs = matrix_df.index.values.tolist()

    u_mat, s_array, v_mat = svd.compute_svd(matrix_df)
    u_mat, s_array, v_mat = svd.reduce_singular_values(u_mat, s_array, v_mat)
    p_mat, q_mat = svd.get_scaled_matrices(u_mat, s_array, v_mat)
    p_mat, q_mat = svd.gradient_descent(matrix_df.iloc.as_matrix(), p_mat, q_mat, 200)

    values = svd.reconstruct_matrix(p_mat, q_mat)

    svd_df = pd.DataFrame(values, index=drugs)

    return svd_df


def compute_rbm(matrix_df):
    """ Returns an indexed matrix, with the Restricted-Boltzman-Machine computed """
    return matrix_df

def compute_pca(matrix_df):
    """ Returns an indexed matrix, with the Principal-Component-Analysis computed """
    return matrix_df
    