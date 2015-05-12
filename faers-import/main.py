"""
    Loads the FAERS data onto a RDBS

    refer to the files ASC_NTS on each trimester folder
"""

import mysql.connector as mysql
import os
import re
import pandas as pd

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
                    report_sources_parser,
                    therapy_parser,
                    indications_parser]

    data_root = './data'

    for quarter_folder in os.listdir(data_root): 
        is_new_model = False
        match = re.match(r'^faers\w*', quarter_folder.lower())

        if match:
            is_new_model = True

        files_dir = data_root + '/' + quarter_folder 

        for in_file in os.listdir(files_dir):
            for pattern, parser in zip(file_patterns, file_parsers):
                match = re.match(pattern, in_file)
                if match:
                    file_path = files_dir + '/' + in_file
                    parser(file_path, is_new_model)

def demographic_parser(filepath, is_new_model):
    """ Parses and inserts the data from the demographic FAERS files """
    if is_new_model:
        generic_parser(filepath)

def drugs_parser(filepath, is_new):
    """ Parses and inserts the data from the drugs FAERS files """
    if is_new_model:
        generic_parser(filepath)

def reactions_parser(filepath, is_new):
    """ Parses and inserts the data from the reactions FAERS files """
    if is_new_model:
        generic_parser(filepath)

def outcomes_parser(filepath, is_new):
    """ Parses and inserts the data from the outcomes FAERS files """
    if is_new_model:
        generic_parser(filepath)

def report_sources_parser(filepath, is_new):
    """ Parses and inserts the data from the report sources FAERS files """
    if is_new_model:
        generic_parser(filepath)

def therapy_parser(filepath, is_new):
    """ Parses and inserts the data from the therapy FAERS files """
    if is_new_model:
        generic_parser(filepath)
    
def indications_parser(filepath, is_new):
    """ Parses and inserts the data from the indications FAERS files """
    if is_new_model:
        generic_parser(filepath)

def generic_parser(filepath):
    data_frame = pd.read_csv(filepath, header=0, sep='$')
    cnx = mysql.connect(user='dpinto', password='dpinto', host='porto.fe.up.pt', database='medline')
    data_frame.to_sql(con=cnx, name='event', if_exists='replace', flavor='mysql')
    cnx.close()

if __name__ == '__main__':
    main()
