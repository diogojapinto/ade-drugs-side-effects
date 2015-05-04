"""
    Script to read and convert R files containing the pmids
"""

import mysql.connector as mysql
from os import listdir
import rpy2.robjects as robjects
import re
import numpy as np

    
def main():
    """ Main function """

    directory = '/home/dpinto/simple-correlation/'

    for in_file in listdir(directory):
        match = re.match(r'pmid_(.*).R', in_file)
        if not match:
            continue

        print('Processing: %s' % match.group(1))

        filename = directory + in_file

        robjects.r['load'](filename)
        pmids = robjects.globalenv['pmids']

        pmids_np_array = np.array(pmids).flatten()
        pmids_np_array = np.unique(pmids_np_array)
        pmids = pmids_np_array.tolist()

        try:
            pmids = filter_pmids(pmids)

            out_file = open('pmid_' + match.group(1) + '.txt', 'w')
            _ = [out_file.write(str(pmid[0]) + '\n') for pmid in pmids]

        except Exception:
            print("error")
            """pmids_new = []

            for i in range(0, len(pmids), 1000):
                pmids_new.append(filter_pmids(pmids[i:i+1000]))

            out_file = open('pmid_' + match.group(1) + '.txt', 'w')
            _ = [out_file.write(str(pmid[0]) + '\n') for pmid in pmids_new]"""
            
    return 0


def filter_pmids(pmids):
    """ Filters the PMIDS by mesh heading """

    pmids_str = '"' + '", "'.join([str(pmid) for pmid in pmids]) + '"'

    query = """ SELECT pmid
                FROM drugs_related_pmids_strong
                WHERE pmid IN (%s);""" % (pmids_str)

    cnx = mysql.connect(user='dpinto', password='dpinto', host='porto.fe.up.pt', database='medline')
    cursor = cnx.cursor()
    cursor.execute(query)
    new_pmids = cursor.fetchall()
    cursor.close()
    cnx.close()

    return new_pmids

if __name__ == '__main__':
    main()
