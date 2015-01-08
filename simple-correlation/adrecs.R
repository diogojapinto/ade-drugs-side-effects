library(RMySQL)

adrecsConn <- dbConnect(MySQL(), user='pcosta', password='pcosta', dbname='ADReCS', host='porto.fe.up.pt')

rs = dbSendQuery(adrecsConn, "SELECT * FROM drug")
drugs = fetch(rs, n=-1)

drugs