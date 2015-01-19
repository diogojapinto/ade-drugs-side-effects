##
## NDC queries
##

getNDCDrugs <- function() {
  query <- 'SELECT proprietary_name, non_proprietary_name, start_marketing_date FROM drug'
  res <- query(ndcConn, query)
  return(res)
}

getDistinctNDCDrugs <- function() {
  query <- 'SELECT DISTINCT(non_proprietary_name) FROM drug'
  res <- query(ndcConn, query)
  return(res)
}

getDrugsByNonProprietaryName <- function(name) {
  query <- paste(c('SELECT proprietary_name, non_proprietary_name, start_marketing_date FROM drug WHERE non_proprietary_name LIKE "%', name, '%"'), collapse="")
  res <- query(ndcConn, query)
  return(res)
}