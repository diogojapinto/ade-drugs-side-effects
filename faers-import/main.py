"""
    Loads the FAERS data onto a RDBS

    refer to the files ASC_NTS on each trimester folder
"""

import mysql.connector as mysql
import os
import re
import pandas as pd
import numpy as np

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
    file_count = 0

    for quarter_folder in os.listdir(data_root): 
        is_new_model = False
        match = re.match(r'^faers\w*', quarter_folder.lower())

        if match:
            is_new_model = True

        files_dir = data_root + '/' + quarter_folder + '/' + 'ascii'

        for in_file in os.listdir(files_dir):
            for pattern, parser in zip(file_patterns, file_parsers):
                match = re.match(pattern, in_file)
                if match:
                    file_path = files_dir + '/' + in_file
                    print("Processing " + in_file)
                    parser(file_path, is_new_model)
                    file_count += 1

    print("Files count: " + str(file_count))

def demographic_parser(filepath, is_new_model):
    """ Parses and inserts the data from the demographic FAERS files """
    if is_new_model:

        dates = ['event_dt', 'mfr_dt', 'init_fda_dt', 'fda_dt', 'rept_dt']

        dtypes = {'primaryid': np.int64,
                  'caseid': np.int64,
                  'caseversion': np.str,
                  'i_f_code': np.str,
                  'rept_cod': np.str,
                  'mfr_num': np.str,
                  'mfr_sndr': np.str,
                  #'age': np.int64,
                  'age_cod': np.str,
                  'gndr_cod': np.str,
                  'e_sub': np.str,
                  #'wt': np.float64,
                  'wt_cod': np.str,
                  'to_mfr': np.str,
                  'occp_cod': np.str,
                  'reporter_country': np.str,
                  'occr_country': np.str}

        data_frame = pd.read_csv(filepath, header=0, sep='$')

        if 'gndr_cod' in data_frame.columns:
            data_frame.rename(columns={'gndr_cod':'sex'}, inplace=True)

        generic_parser(filepath, 'event', data_frame)

def drugs_parser(filepath, is_new_model):
    """ Parses and inserts the data from the drugs FAERS files """
    #if is_new_model:
    #    generic_parser(filepath)

def reactions_parser(filepath, is_new_model):
    """ Parses and inserts the data from the reactions FAERS files """
    #if is_new_model:
    #    generic_parser(filepath)

def outcomes_parser(filepath, is_new_model):
    """ Parses and inserts the data from the outcomes FAERS files """
    #if is_new_model:
    #    generic_parser(filepath)

def report_sources_parser(filepath, is_new_model):
    """ Parses and inserts the data from the report sources FAERS files """
    #if is_new_model:
    #    generic_parser(filepath)

def therapy_parser(filepath, is_new_model):
    """ Parses and inserts the data from the therapy FAERS files """
    #if is_new_model:
    #    generic_parser(filepath)
    
def indications_parser(filepath, is_new_model):
    """ Parses and inserts the data from the indications FAERS files """
    #if is_new_model:
    #    generic_parser(filepath)

def generic_parser(filepath, table, data_frame):
    """ Directly dumps a dataframe on a mySQL database """

    cnx = mysql.connect(user='dpinto', password='dpinto', host='porto.fe.up.pt', database='faers')
    cur = cnx.cursor()

    names = list(data_frame.columns.values)
    bracketed_names = ['`' + column + '`' for column in names]
    col_names = ','.join(bracketed_names)
    wildcards = ','.join([r'%s'] * len(names))
    insert_query = "REPLACE INTO %s (%s) VALUES (%s)" % (
        table, col_names, wildcards)

    data_frame = data_frame.where((pd.notnull(data_frame)), None)

    cur.executemany(insert_query, data_frame.values.tolist())
    cnx.commit()
    cur.close()
    cnx.close()

if __name__ == '__main__':
    main()
