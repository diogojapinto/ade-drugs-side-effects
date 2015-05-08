import mysql.connector as mysql
import sys

def get_abstract(pmid):
    """ Retrieves the abstract for a given pmid """
    print(pmid)
    cnx = mysql.connect(user='dpinto', password='dpinto', host='porto.fe.up.pt', database='medline')

    query = """SELECT article_title, abstract_text
               FROM medline_citation
               WHERE pmid = %s"""
    
    cursor = cnx.cursor()
    cursor.execute(query, (pmid,))

    elem = cursor.fetchone()

    title, abstract = elem[0], elem[1]

    cursor.close()
    cnx.close()

    return title, abstract

if __name__ == '__main__':
    print(get_abstract(sys.argv[1]))
