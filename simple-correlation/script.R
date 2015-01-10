library("RMySQL")

##
## Function to connect to databases (default is for ADReCS)
##
getConnection <- function(user='pcosta', password='pcosta', dbname, host='porto.fe.up.pt'){
  conn <- dbConnect(MySQL(), user=user, password=password, dbname=dbname, host=host)
  return(conn)
}

##
## Base function for querying the databases
##
query <- function(con, query, n=-1){
  res <- fetch(dbSendQuery(con,query),n=n)
  return(res)
}

##
## Connections
##
medlineConn <- getConnection(dbname='medline');
adresConn <- getConnection(dbname='medline');
ndcConn <- getConnection(dbname='ndc_db');

##
## ADReCS queries
##

getDrugSynonyms <- function(con, drugId){
  query <- paste('SELECT * FROM drug_synonym WHERE drug like "', drugId, sep="")
  query <- paste(query, '"', sep="")
  syns <- query(con, query)
  return(syns)
}

getDrugs <- function(con, drug=""){
  
  if(drug=="")
    qs <- c("SELECT * FROM drug")
  else
    qs <- c('SELECT * FROM drug WHERE id = "', drug, '"')
  query <- paste(qs,collapse="")
  drugs <- query(con,query)
  return(drugs)
}

getDrugsByName <- function(con, drugName){
  qs <- c('SELECT DISTINCT(drug.id) FROM drug JOIN drug_synonym ON drug.id = drug_synonym.drug WHERE drug.name like "', drugName, '" OR drug_synonym.syn like "', drugName, '"')
  query <- paste(qs, collapse="") 
  res <- query(con, query)
  return(res)
}

rs <- dbSendQuery(getConnection(), "SELECT drug.id, drug.name, drug_synonym.syn FROM drug JOIN drug_synonym ON drug.id = drug_synonym.drug")
drugs <- fetch(rs, n=-1)

##
## NDC queries
##

##
## Medline
##

