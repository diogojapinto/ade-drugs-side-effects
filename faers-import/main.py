"""
    Loads the FAERS data onto a RDBS
"""

import mysql.connector as mysql
import os
import re

def main():
    """ Main function here """

    file_patterns = [r'^DEMO\w*.txt$',
                     r'^DRUG\w*.txt$',
                     r'^REAC\w*.txt$',
                     r'^OUTC\w*.txt$',
                     r'^RPSR\w*.txt$',
                     r'^THER\w*.txt$',
                     r'^INDI\w*.txt$']

    file_parsers = [demographic_parser,
                    drugs_parser,
                    reactions_parser,
                    outcomes_parser,
                    reports_sources_parser,
                    therapy_parser,
                    indications_parser]

    data_root = './data'

    for quarter_folder in os.listdir(data_root): 
        is_new = False
        match = re.match(r'^faers\w*', quarter_folder.lower())
        if match:
            is_new = True

        files_dir = data_root + '/' + quarter_folder

        for in_file in os.listdir(files_dir):
            

        for pat, fn in zip(file_patterns, file_parsers):
            match = re.match(pat, in_file)
            if (match)


if __name__ == '__main__':
    main()
