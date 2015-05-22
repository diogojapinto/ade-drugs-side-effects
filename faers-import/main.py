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

    file_patterns = [r'^DEMO\w*.(txt|TXT)$',
                     r'^DRUG\w*.(txt|TXT)$',
                     r'^REAC\w*.(txt|TXT)$',
                     r'^OUTC\w*.(txt|TXT)$',
                     r'^RPSR\w*.(txt|TXT)$',
                     r'^THER\w*.(txt|TXT)$',
                     r'^INDI\w*.(txt|TXT)$']

    file_parsers = [demographic_parser,
                    drugs_parser,
                    reactions_parser,
                    outcomes_parser,
                    report_sources_parser,
                    therapy_parser,
                    indications_parser]

    data_root = './data'
    file_count = 0
    database = load_parsed_files()

    for quarter_folder in os.listdir(data_root):
        files_dir = data_root + '/' + quarter_folder + '/' + 'ascii'

        selected_files = []

        for in_file in os.listdir(files_dir):
            for i, (pattern, parser) in enumerate(zip(file_patterns, file_parsers)):
                match = re.match(pattern, in_file)

                if match:
                    file_path = files_dir + '/' + in_file
                    # put the demographic file first
                    if i == 0:
                        selected_files.insert(0, (parser, file_path))
                    else:
                        selected_files.append((parser, file_path))

        for parser, in_file in selected_files:
            if in_file in database:
                continue

            print("Processing " + in_file)
            data_frame = pd.read_csv(in_file, header=0, sep='$')
            data_frame.columns = [x.lower() for x in data_frame.columns]
            parser(data_frame)
            file_count += 1
            add_parsed_file(in_file)
            database.add(in_file)
                    

    print("Files count: " + str(file_count))

def demographic_parser(data_frame):
    """ Parses and inserts the data from the demographic FAERS files """
    
    change_cols = {'gndr_cod': 'sex',
                   'isr': 'primaryid',
                   'case': 'caseid',
                   'i_f_cod': 'i_f_code'}
    del_cols = ['foll_seq', 'image', 'death_dt', 'confid']

    rename_columns(data_frame, change_cols)
    delete_columns(data_frame, del_cols)

    generic_parser('event', data_frame)

def drugs_parser(data_frame):
    """ Parses and inserts the data from the drugs FAERS files """
    
    change_cols = {'isr': 'primaryid',
                   'case': 'caseid'}

    rename_columns(data_frame, change_cols)

    generic_parser('event_drugs', data_frame)

def reactions_parser(data_frame):
    """ Parses and inserts the data from the reactions FAERS files """
    
    change_cols = {'isr': 'primaryid',
                   'case': 'caseid',
                   'pt': 'medra_pt'}

    rename_columns(data_frame, change_cols)

    generic_parser('event_reactions', data_frame)

def outcomes_parser(data_frame):
    """ Parses and inserts the data from the outcomes FAERS files """
    change_cols = {'isr': 'primaryid',
                   'case': 'caseid'}

    rename_columns(data_frame, change_cols)

    generic_parser('event_outcomes', data_frame)

def report_sources_parser(data_frame):
    """ Parses and inserts the data from the report sources FAERS files """
    
    change_cols = {'isr': 'primaryid',
                   'case': 'caseid'}

    rename_columns(data_frame, change_cols)

    generic_parser('event_report_sources', data_frame)

def therapy_parser(data_frame):
    """ Parses and inserts the data from the therapy FAERS files """
    change_cols = {'isr': 'primaryid',
                   'case': 'caseid',
                   'drug_seq': 'dsg_drug_seq'}

    rename_columns(data_frame, change_cols)

    generic_parser('event_therapy', data_frame)
    
def indications_parser(data_frame):
    """ Parses and inserts the data from the indications FAERS files """
    change_cols = {'isr': 'primaryid',
                   'case': 'caseid',
                   'drug_seq': 'indi_drug_seq',
                   'indi_pt': 'medra_indi_pt'}

    rename_columns(data_frame, change_cols)
    
    generic_parser('event_indications', data_frame)

def generic_parser(table, data_frame):
    """ Directly dumps a dataframe on a mySQL database """

    cnx = mysql.connect(user='dpinto', password='dpinto', host='porto.fe.up.pt', database='faers')
    cur = cnx.cursor()

    names = list(data_frame.columns.values)
    bracketed_names = ['`' + column + '`' for column in names]
    col_names = ','.join(bracketed_names)
    wildcards = ','.join([r'%s'] * len(names))
    insert_query = "REPLACE INTO %s (%s) VALUES (%s)" % (
        table, col_names, wildcards)

    data_frame = data_frame[pd.notnull(data_frame[0])]
    data_frame = data_frame.where((pd.notnull(data_frame)), None)

    cur.executemany(insert_query, data_frame.values.tolist())
    cnx.commit()
    cur.close()
    cnx.close()

def rename_columns(data_frame, names_dict):
    """ Renames the columns that exist on the dataframe """

    for old_name, new_name in names_dict.items():
        if old_name in data_frame.columns:
            data_frame.rename(columns={old_name: new_name}, inplace=True)

def delete_columns(data_frame, names_list):
    """ Deletes the specified columns on the dataframe """
    for name in names_list:
        if name in data_frame.columns:
            data_frame.drop(name, axis=1, inplace=True)

def load_parsed_files():
    """ Loads the previously parsed files, jumping them """
    database = set([line.strip() for line in open('db.txt', 'r')])
    return database

def add_parsed_file(in_file):
    """ Adds a new parsed file record to the database """
    with open('db.txt', 'a') as out_file:
        out_file.write(in_file + '\n')

if __name__ == '__main__':
    main()
