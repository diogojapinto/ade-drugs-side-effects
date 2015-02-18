"""
    Library for building graphs using NetworkX
"""

# import networkx as nx
import numpy as np

def build_drugs_dict(drugs):
    """ Builds a dictionary that maps drug ids to indexes of the graph's matrix"""
    return {id: index for (index, id) in enumerate(drugs)}
    

def build_graph(cursor, drugs_dict):
    """Build an adjancency matrix in a drug-to-drug manner"""

    # initialize the dictionary and matrix
    nr_drugs = len(drugs_dict)
    graph = np.zeros(shape=(nr_drugs, nr_drugs))

    current_edge = ""
    current_vertexes = []
    for (vertex1, edge) in cursor:

        if edge != current_edge:
            current_vertexes = []
            current_edge = edge

        for vertex2 in current_vertexes:
            index1 = drugs_dict[vertex1]
            index2 = drugs_dict[vertex2]

            # update the values on the matrix, already envisioning Spectral Clustering
            graph[index1][index2] -= 1
            graph[index2][index1] -= 1
            graph[index1][index1] += 1
            graph[index2][index2] += 1

        current_vertexes.append(vertex1)


    return graph
