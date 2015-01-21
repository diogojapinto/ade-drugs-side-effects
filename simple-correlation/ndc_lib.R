##
## NDC queries
##

getNDCDrugs <- function() {
  ndcConn <- getConnection(dbname='ndc_db')
  query <- 'SELECT proprietary_name, non_proprietary_name, start_marketing_date FROM drug'
  res <- query(ndcConn, query)
  dbDisconnect(ndcConn)
  return(res)
}

getDistinctNDCDrugs <- function() {
  ndcConn <- getConnection(dbname='ndc_db')
  query <- 'SELECT DISTINCT(non_proprietary_name) FROM drug'
  res <- query(ndcConn, query)
  dbDisconnect(ndcConn)
  return(res)
}

getDrugsByNonProprietaryName <- function(name) {
  ndcConn <- getConnection(dbname='ndc_db')
  query <- paste(c('SELECT proprietary_name, non_proprietary_name, start_marketing_date FROM drug WHERE non_proprietary_name LIKE "%', name, '%"'), collapse="")
  res <- query(ndcConn, query)
  dbDisconnect(ndcConn)
  return(res)
}