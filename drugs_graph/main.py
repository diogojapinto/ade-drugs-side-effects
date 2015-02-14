import adrecs_interface as ai
import pickle as pk

def main():

    try:
        graph = pk.load(open('graph.txt', 'rb'))
    except FileNotFoundError:
        graph = ai.get_connections_drug_to_drug()
        pk.dump(graph, open('graph.txt', 'wb'))
    
    print(graph.nodes())
    print(graph.edges())

if __name__ == "__main__":
    main()
