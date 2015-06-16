"""
    Library for building graphs using NetworkX
"""

# import networkx as nx
import numpy as np
import atc_code as atc
from constants import ADRS_WEIGHT

def build_drugs_dict(drugs):
    """ Builds a dictionary that maps drug ids to indexes of the graph's matrix"""
    return {ident[0]: index for (index, ident) in enumerate(drugs)}

def build_adrs_dict(adrs):
    """ Builds a dictionary that maps adr ids to indexes of the graph's matrix"""
    return {ident[0]: index for (index, ident) in enumerate(adrs)}
    

def build_graph(cursor, drugs_dict):
    """Build an adjancency matrix in a drug-to-drug manner"""

    # initialize the dictionary and matrix
    nr_drugs = len(drugs_dict)
    graph = np.zeros(shape=(nr_drugs, nr_drugs))

    current_edge = ""
    current_vertexes = []

    cursor = cursor.fetchall()
    for (vertex1, edge) in cursor:

        if edge != current_edge:
            current_vertexes = []
            current_edge = edge

        for vertex2 in current_vertexes:
            index1 = drugs_dict[vertex1]
            index2 = drugs_dict[vertex2]

            # update the values on the matrix, already envisioning Spectral Clustering
            # graph[index1][index2] -= 1
            # graph[index2][index1] -= 1
            # graph[index1][index1] += 1
            # graph[index2][index2] += 1

            if graph[index1][index2] != 1:
                graph[index1][index2] = 1
                graph[index2][index1] = 1
                graph[index1][index1] += 1
                graph[index2][index2] += 1

        current_vertexes.append(vertex1)


    return graph

def build_bipartite_graph(cursor, drugs_dict, adrs_dict):
    """Build an adjancency matrix in a drug-to-adr manner"""
    # initialize the dictionary and matrix
    nr_drugs = len(drugs_dict)
    nr_adrs = len(adrs_dict)
    graph = np.zeros(shape=(nr_drugs, nr_adrs))

    for (drug, adr) in cursor.fetchall():
        index1 = drugs_dict[drug]
        index2 = adrs_dict[adr]

        graph[index1, index2] = ADRS_WEIGHT

    return graph

def build_atc_mat(atc_codes):
    graph = np.array([atc.Atc_code(code).get_descriptor() for code in atc_codes])
    return graph
