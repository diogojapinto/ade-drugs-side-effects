library("DBI")
library("RMySQL")

##
## init
##
for(conn in dbListConnections(MySQL())) {
  dbDisconnect(conn)
}

##
## Function to connect to databases
##
getConnection <- function(user='pcosta', password='pcosta', dbname, host='localhost'){
  conn <- dbConnect(MySQL(), user=user, password=password, dbname=dbname, host=host)
  return(conn)
}

##
## Base function for querying the databases
##
query <- function(con, query, n=-1){
  rs <- dbSendQuery(con,query)
  res <- dbFetch(rs,n=n)
  while(n != -1 && !dbHasCompleted(rs)){
    res <- rbind(res, dbFetch(rs, n))
    print(nrow(res))
  }
  dbClearResult(rs)
  return(res)
}

##
## Cleanup
##
clean <- function() {
  dbDisconnect(medlineConn)
  dbDisconnect(adresConn)
  dbDisconnect(ndcConn)
}

##
## Connections
##
adresConn <- getConnection(dbname='ADReCS')