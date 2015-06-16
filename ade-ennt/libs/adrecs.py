"""
    Library for interacting with ADReCS database
"""

import mysql.connector as mysql
import numpy as np
import pandas as pd


def get_connection():
    """ Establishes a connection to the ADReCS database """
    cnx = mysql.connect(user='dpinto', password='dpinto', host='porto.fe.up.pt', database='ADReCS')
    return cnx


def close_connection(cnx):
    """ Closes a previously established connection """
    cnx.close()


def get_drug_names(ident):
    """ Retrieves the corresponding drug name to an ident """

    query = """SELECT drug.name AS name
               FROM drug
               WHERE drug.id = %s

               UNION ALL

               SELECT drug_synonym.syn as name
               FROM drug_synonym
               WHERE drug_synonym.drug = %s"""
    
    cnx = get_connection()
    cursor = cnx.cursor()

    cursor.execute(query, (ident,))
    names = [x[0] for x in cursor.fetchall()]

    cursor.close()
    close_connection(cnx)

    return names


def get_adr_names(ident):
    """ Retrieves the corresponding adr name to an ident """

    query = """SELECT adr.term AS name
               FROM adr
               WHERE adr.id = %s

               UNION ALL

               SELECT adr_synonym.syn AS name
               FROM adr_synonym
               WHERE adr_synonym.adr = %s"""
    
    cnx = get_connection()
    cursor = cnx.cursor()

    cursor.execute(query, (ident,))
    names = [x[0] for x in cursor.fetchall()]

    cursor.close()
    close_connection(cnx)

    return names


def get_all_drugs_ids():
    """ Retrieves all the identifiers of drugs on the database """

    query = """SELECT DISTINCT drug.id
               FROM drug
               ORDER BY drug.id, drug.name"""
    
    cnx = get_connection()
    cursor = cnx.cursor()
    cursor.execute(query)

    ids = [x[0] for x in cursor.fetchall()]

    cursor.close()
    close_connection(cnx)

    return ids


def get_all_adrs_ids():
    """ Retrieves all the identifiers of adrs on the database """

    query = """SELECT DISTINCT adr.id
               FROM adr
               ORDER BY adr.id, adr.term"""
    
    cnx = get_connection()
    cursor = cnx.cursor()
    cursor.execute(query)

    ids = [x[0] for x in cursor.fetchall()]

    cursor.close()
    close_connection(cnx)

    return ids


def get_drug_adr_matrix(level=4):
    """ Retrieves the drug-adr connections, and builds a bipartite matrix based on it """

    regex_levels = {
        1: '^..$',
        2: '^..[[.full-stop.]]..$',
        3: '^..[[.full-stop.]]..[[.full-stop.]]..$',
        4: '^..[[.full-stop.]]..[[.full-stop.]]..[[.full-stop.]]...$',
    }


    query = """SELECT drug_id, adr_id
               FROM drug_adr INNER JOIN 
               WHERE adr_id REGEXP """ + regex_levels[level]

    cnx = get_connection()
    cursor = cnx.cursor()
    cursor.execute(query)

    matrix_df = build_matrix(cursor)

    cursor.close()
    close_connection(cnx)

    return matrix_df


def build_matrix(cursor):
    """Build an adjacency matrix in a drug-to-adr manner"""

    # initialize the dictionary and matrix

    drugs = get_all_drugs_ids()
    adrs = get_all_adrs_ids()

    drugs_dict = {ident: index for (index, ident) in enumerate(drugs)}
    adrs_dict = {ident: index for (index, ident) in enumerate(adrs)}

    nr_drugs = len(drugs_dict)
    nr_adrs = len(adrs_dict)
    matrix = np.zeros(shape=(nr_drugs, nr_adrs))

    for (drug, adr) in cursor.fetchall():
        index1 = drugs_dict[drug]
        index2 = adrs_dict[adr]

        matrix[index1, index2] = 1

    matrix_df = pd.DataFrame(matrix, index=drugs_dict, columns=adrs_dict)

    return matrix_df


def get_drug_id(drug):
    """ Retrieves the id of the drug, looking both for original name and synonyms """

    query = """SELECT drug.id AS id
               FROM drug
               WHERE drug.name LIKE %s

               UNION ALL

               SELECT drug_synonym.drug as id
               FROM drug_synonym
               WHERE drug_synonym.syn LIKE %s"""
    
    cnx = get_connection()
    cursor = cnx.cursor()

    cursor.execute(query, (drug,))
    ids = [x[0] for x in cursor.fetchall()]

    cursor.close()
    close_connection(cnx)

    return ids


def get_adr_id(adr):
    """ Retrieves the id of the drug, looking both for original name and synonyms """

    query = """SELECT adr.id AS id
               FROM adr
               WHERE adr.term LIKE %s

               UNION ALL

               SELECT adr_synonym.adr as id
               FROM adr_synonym
               WHERE adr_synonym.syn LIKE %s"""
    
    cnx = get_connection()
    cursor = cnx.cursor()

    cursor.execute(query, (adr,))
    ids = [x[0] for x in cursor.fetchall()]

    cursor.close()
    close_connection(cnx)

    return ids


def get_drugs_name_to_id_dict():
    """ Returns a dictionary that enables the conversion from drug name to id """

    query = """SELECT drug.name as name, drug.id AS id
               FROM drug

               UNION ALL

               SELECT drug_synonym.syn as name, drug_synonym.drug as id
               FROM drug_synonym"""
    
    cnx = get_connection()
    cursor = cnx.cursor()

    cursor.execute(query)
    drugs_dict = {x[0].lower(): x[1] for x in cursor.fetchall()}

    cursor.close()
    close_connection(cnx)

    return drugs_dict
