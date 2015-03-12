"""
    Interface for connecting to ADReCS database
"""

import mysql.connector as mysql
import graph_builder as gb


def get_connection():
    """ Establishes a connection to the ADReCS database """
    cnx = mysql.connect(user='dpinto', password='dpinto', host='porto.fe.up.pt', database='ADReCS')
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
    cursor.execute(query, ident)

    term = cursor.fetchone()['adr.term']

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
    cursor.execute(query, ident)

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
