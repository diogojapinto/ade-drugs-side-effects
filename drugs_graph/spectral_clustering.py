"""
Performs Spectral Clustering on an square matrix representing a graph

Source:
    http://infolab.stanford.edu/~ullman/mmds/book.pdf
    and corresponding MOOC at Coursera

Steps:  1. Pre-process
            construct matrix representation of the graph (already done)

        2. Decomposition
            compute eigenvalues and eigenvectors of the matrix
            map each point to a lower-dimensional representation based on one or more eigenvectors

        3. Grouping
            assign points to two or more clusters, based on the new representation (use k-means)
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


def get_clusters(graph, nr_clusters):
    """ Retrieves the clusters achieved by multi-level Spectral Clustering """
    _, eigenvectors = np.linalg.eig(graph)

    # plt.plot(sorted(eigenvectors[1, :]))
    # plt.show()

    k_means = KMeans(n_clusters=nr_clusters)
    k_means.fit(eigenvectors)
    y_pred = k_means.predict(eigenvectors)


    #plt.scatter(range(len(eigenvectors[1, :])), eigenvectors[1, :], c=y_pred)
    #plt.show()

    return y_pred

