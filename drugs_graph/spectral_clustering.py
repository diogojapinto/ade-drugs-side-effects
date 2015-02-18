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

def get_clusters():
    pass