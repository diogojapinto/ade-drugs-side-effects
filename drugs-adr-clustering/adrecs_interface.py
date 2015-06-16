"""
    Interface for connecting to ADReCS database
"""

import mysql.connector as mysql
import graph_builder as gb
import atc_code as atc
import pandas as pd
import pickle as pk


def get_connection():
    """ Establishes a connection to the ADReCS database """
    cnx = mysql.connect(user='pcosta', password='pcosta', host='porto.fe.up.pt', database='ADReCS')
    return cnx


def close_connection(cnx):
    """ Closes a previously established connection """
    cnx.close()


def get_adr_name(ident):
    """ Retrieves the corresponding adr name to an ident """
    query = """SELECT adr.term
               FROM adr
               WHERE adr.id = %s"""
    
    cnx = get_connection()
    cursor = cnx.cursor()
    cursor.execute(query, (ident,))

    term = cursor.fetchone()[0]

    cursor.close()
    close_connection(cnx)

    return term


def get_drug_name(ident):
    """ Retrieves the corresponding drug name to an ident """
    query = """SELECT drug.name
               FROM drug
               WHERE drug.id = %s"""
    
    cnx = get_connection()
    cursor = cnx.cursor()
    cursor.execute(query, (ident,))

    term = cursor.fetchone()[0]

    cursor.close()
    close_connection(cnx)

    return term

def get_all_drugs_ids():
    """ Retrieves all the identifiers of drugs on the database """
    query = """SELECT DISTINCT drug.id
               FROM drug"""
    
    cnx = get_connection()
    cursor = cnx.cursor()
    cursor.execute(query, id)

    ids = cursor.fetchall()

    cursor.close()
    close_connection(cnx)

    return ids

def get_all_adrs_ids():
    """ Retrieves all the identifiers of adrs on the database """
    query = """SELECT DISTINCT adr.id
               FROM adr"""
    
    cnx = get_connection()
    cursor = cnx.cursor()
    cursor.execute(query, id)

    ids = cursor.fetchall()

    cursor.close()
    close_connection(cnx)

    return ids

def get_all_drugs_names():
    """ Retrieves all the names of drugs on the database """
    query = """SELECT DISTINCT drug.name
               FROM drug"""
    
    cnx = get_connection()
    cursor = cnx.cursor()
    cursor.execute(query, id)

    names = cursor.fetchall()

    cursor.close()
    close_connection(cnx)

    return names

def get_drug_atc(drug_id):
    """ Returns the atc_code of a drug """

    query = """SELECT atc
               FROM drug 
               WHERE id = %s"""

    cnx = get_connection()
    cursor = cnx.cursor()
    cursor.execute(query, (drug_id,))

    atc_code = cursor.fetchone()[0]

    cursor.close()
    close_connection(cnx)

    return atc_code

def get_connections_drug_to_drug():
    """ Retrieves the drug-adr connections, and builds a graph on it (drug-drug) """
    query = """SELECT drug_id, adr_id
               FROM drug_adr
               ORDER BY adr_id"""

    cnx = get_connection()
    cursor = cnx.cursor()
    cursor.execute(query)

    drugs_dict = gb.build_drugs_dict(get_all_drugs_ids())
    graph = gb.build_graph(cursor, drugs_dict)

    cursor.close()
    close_connection(cnx)

    return graph

def get_drug_adr_matrix():
    """ Retrieves the drug-adr connections, and builds a bipartite matrix based on it """
    query = """SELECT drug_id, adr_id
               FROM drug_adr
               WHERE adr_id REGEXP '^..[[.full-stop.]]..[[.full-stop.]]..[[.full-stop.]]...$'"""

    cnx = get_connection()
    cursor = cnx.cursor()
    cursor.execute(query)

    drugs = get_all_drugs_ids()
    
    drugs_dict = gb.build_drugs_dict(drugs)
    adrs_dict = gb.build_drugs_dict(get_all_adrs_ids())
    matrix = gb.build_bipartite_graph(cursor, drugs_dict, adrs_dict)

    cursor.close()
    close_connection(cnx)

    atc_codes = [get_drug_atc(drug_id) for drug_id in drugs]
    atc_mat = gb.build_atc_mat(atc_codes)

    matrix_df = pd.DataFrame(matrix, index=drugs_dict, columns=adrs_dict)
    atc_df = pd.DataFrame(atc_mat, index=drugs_dict, columns=atc.first_level_codes)

    matrix_df = pd.concat([matrix_df,atc_df], axis=1, join_axes=[matrix_df.index])

    return matrix_df