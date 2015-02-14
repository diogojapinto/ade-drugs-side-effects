"""
    Interface for connecting to ADReCS database
"""

import mysql.connector as mysql
import graph_builder as gb


def get_connection():
    cnx = mysql.connect(user='dpinto', password='dpinto',
                                  host='porto.fe.up.pt',
                                  database='ADReCS')
    return cnx

def close_connection(cnx):
    cnx.close()

def get_connections_drug_to_drug():

    query = ("""SELECT drug.name AS drug, adr.term AS adr
                FROM drug
                    INNER JOIN drug_adr ON drug.id = drug_id 
                    INNER JOIN adr ON adr_id = adr.id 
                ORDER BY adr""")

    cnx = get_connection()

    cursor = cnx.cursor()

    cursor.execute(query)

    graph = gb.build_drug_to_drug(cursor)

    cursor.close()
    close_connection(cnx)

    return graph
