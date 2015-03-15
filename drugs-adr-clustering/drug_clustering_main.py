"""
    Main module. Start here
"""

import pickle as pk
import adrecs_interface as ai
import spectral_clustering as sc

def main():
    """ Entry function.
        When computation is too long, saves objects to files"""

    try:
        graph = pk.load(open('data/graph.p', 'rb'))
    except FileNotFoundError:
        graph = ai.get_connections_drug_to_drug()
        pk.dump(graph, open('data/graph.p', 'wb'))

    fout = open("clusters.log", "w")

    fout.write("Number of elements per cluster\n\n")

    for nr_clusters in range(2, 12):
        clusters = sc.get_clusters(graph, nr_clusters)
        fout.write("Cluster " + str(nr_clusters) + "\n")

        for i in range(nr_clusters):
            fout.write("\t" + str(i) + ": " + str(sum(clusters == i)) + "\n")

        fout.write("\n\n")
    
    fout.close()
    

if __name__ == "__main__":
    main()
