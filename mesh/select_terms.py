"""
    Selects from the MESH Tree all of the components inside any category, and saves it to selected_mesh.txt
"""

from sys import argv

def main():
    """ Main function """

    args = argv[1:]

    out_file = open("selected_mesh.txt", "w")

    for line in open("mtrees2015.txt"):
        term, code = line.strip().split(';')
        if code[0] in args:
            out_file.write(term + '\n')





if __name__ == "__main__":
    main()
