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
getConnection <- function(user='pcosta', password='pcosta', dbname, host='porto.fe.up.pt'){
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
  }
  dbClearResult(rs)
  return(res)
}