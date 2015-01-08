library("RMySQL")

medlineConn <- dbConnect(MySQL(), user='dpinto', password='dpinto', dbname='medline', host='porto.fe.up.pt')

# dbListTables(medlineConn)

