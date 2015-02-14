"""
    Library for building graphs using NetworkX
"""

import networkx as nx

def build_drug_to_drug(cursor):
    """Build a NetworkX Graph in a drug-to-drug manner"""

    graph = nx.MultiGraph()

    f = open('edges.txt', 'w')
    current_adr = ""
    current_drugs = []
    for (drug1, adr) in cursor:

        if adr != current_adr:
            current_drugs = []
            current_adr = adr

        for drug2 in current_drugs:
            # graph.add_edge(drug1, drug2, label=adr)
            f.write(drug1 + '\t' + drug2 + '\t' + adr + '\n')

        current_drugs.append(drug1)

    f.close()

    return graph

