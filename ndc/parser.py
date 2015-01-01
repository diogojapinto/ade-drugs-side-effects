"""
  parses a text file from National Code Directory, containing drugs and introduction dates

"""

import mysql.connector

def main():
  file = open('product.txt', 'r')

  cnx = mysql.connector.connect(user='dpinto', password='dpinto',
                                host='192.168.101.172',
                                database='ndc_db')

  drug_cmd = ("""INSERT INTO drug 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""")

  rows = file.readlines()
  for r in rows[1:2]:

    cursor = cnx.cursor()

    data = r.split('\t')[:-1]            # to remove the last element (\r\n)


    # format the data strings accordingly

    if data[8] != '':
      data[8] = data[8][:4] + '-' + data[8][4:6] + '-' + data[8][6:]
    
    if data[9] != '':
      data[9] = data[9][:4] + '-' + data[9][4:6] + '-' + data[9][6:]

    # print(*data, sep='\n')

    try:
      cursor.execute(drug_cmd, tuple(data))
    except:
      print("Error inserting data: " + data[0])
      conn.rollback()

  cnx.commit()
        
  cnx.close()



if __name__ == '__main__':
  main()
