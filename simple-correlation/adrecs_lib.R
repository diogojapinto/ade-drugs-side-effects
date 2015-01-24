##
## ADReCS queries
##

getDrugSynonyms <- function(drugId){
  adresConn <- getConnection(dbname='ADReCS')
  query <- paste('SELECT * FROM drug_synonym WHERE drug like "', drugId, sep="")
  query <- paste(query, '"', sep="")
  syns <- query(adresConn, query)
  dbDisconnect(adresConn)
  return(syns)
}

getDrugs <- function(drug=""){
  adresConn <- getConnection(dbname='ADReCS')
  if(drug=="")
    qs <- c("SELECT * FROM drug")
  else
    qs <- c('SELECT * FROM drug WHERE id = "', drug, '"')
  query <- paste(qs,collapse="")
  drugs <- query(adresConn,query)
  dbDisconnect(adresConn)
  return(drugs)
}

getDrugsByName <- function(drugName){
  adresConn <- getConnection(dbname='ADReCS')
  qs <- c('SELECT DISTINCT(drug.id) FROM drug JOIN drug_synonym ON drug.id = drug_synonym.drug WHERE drug.name like "', drugName, '" OR drug_synonym.syn like "', drugName, '"')
  query <- paste(qs, collapse="") 
  res <- query(adresConn, query)
  dbDisconnect(adresConn)
  return(res)
}

getDrugsAdrs <- function(drug, synonyms=FALSE){
  adresConn <- getConnection(dbname='ADReCS')
  qs <- c('SELECT adr.term FROM adr JOIN drug_adr ON adr.id = drug_adr.adr_id WHERE drug_adr.drug_id = "', drug, '"')
  if(synonyms) {
    qs <- c(qs, ' UNION SELECT syn as term FROM adr_synonym JOIN adr ON adr.id = adr_synonym.adr JOIN drug_adr ON drug_adr.adr_id = adr.id WHERE drug_adr.drug_id = "', drug, '"')
  }
  query <- paste(qs, collapse="")
  res <- query(adresConn, query)
  dbDisconnect(adresConn)
  return(res)
}