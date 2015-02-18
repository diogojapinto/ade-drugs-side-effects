"""
    Main module. Start here
"""

import adrecs_interface as ai
import pickle as pk

def main():
    """ Entry function.
        When computation is too long, saves objects to files"""

    try:
        graph = pk.load(open('graph.p', 'rb'))
    except FileNotFoundError:
        graph = ai.get_connections_drug_to_drug()
        pk.dump(graph, open('graph.p', 'wb'))
    

if __name__ == "__main__":
    main()
