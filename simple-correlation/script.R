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
  res <- fetch(dbSendQuery(con,query),n=n)
  return(res)
}

##
## Connections
##
medlineConn <- getConnection(dbname='medline');
adresConn <- getConnection(dbname='ADReCS');
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

getDrugsAdrs <- function(con, drug){
  qs <- c('SELECT adr.term FROM adr JOIN drug_adr ON adr.id = drug_adr.adr_id WHERE drug_adr.drug_id = "', drug, '" UNION SELECT syn as term FROM adr_synonym JOIN adr ON adr.id = adr_synonym.adr JOIN drug_adr ON drug_adr.adr_id = adr.id WHERE drug_adr.drug_id = "', drug, '"')
  query <- paste(qs, collapse="")
  res <- query(con, query)
  return(res)
}

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

##
## Medline
##

getSelectedRecordsInfo <- function(pmids) {
  qs <- c("SELECT pmid, date_created 
          FROM medline_citation 
          WHERE pmid IN (",
          paste0(pmids, collapse=","),
          ") ORDER BY date_created")
  query <- paste(qs, collapse="")
  res <- query(medlineConn, query)
  return(res)
}

getInterestingRecords <- function(terms) {
  terms_str <- paste0(terms, collapse="\" \"")
  
  qs <- c("SELECT pmid
          FROM medline_citation
          WHERE MATCH(article_title, abstract_text)
          AGAINST ('\"",
          terms_str,
          "\"' IN BOOLEAN MODE)")
  query <- paste(qs, collapse="")
  
  res <- query(medlineConn, query)
  
  qs <- c("SELECT pmid
          FROM medline_keyword_list
          WHERE MATCH(keyword)
          AGAINST ('\"",
          terms_str,
          "\"' IN BOOLEAN MODE)")
  query <- paste(qs, collapse="")
  res <- rbind(res, query(medlineConn, query))
  
  qs <- c("SELECT pmid
          FROM medline_mesh_heading
          WHERE MATCH(descriptor_name)
          AGAINST ('\"",
          terms_str,
          "\"' IN BOOLEAN MODE)")
  query <- paste(qs, collapse="")
  res <- rbind(res, query(medlineConn, query))
  
  qs <- c("SELECT pmid
          FROM medline_mesh_heading_qualifier
          WHERE MATCH(descriptor_name)
          AGAINST ('\"",
          terms_str,
          "\"' IN BOOLEAN MODE)")
  query <- paste(qs, collapse="")
  res <- rbind(res, query(medlineConn, query))
  
  qs <- c("SELECT pmid
          FROM medline_citation_other_abstract
          WHERE MATCH(abstract_text)
          AGAINST ('\"",
          terms_str,
          "\"' IN BOOLEAN MODE)")
  query <- paste(qs, collapse="")
  res <- rbind(res, query(medlineConn, query))
  
  return(res)
}


##
## Execution
##

# retrieveData('pravastatin')

retrieveData <- function(name) {
  # 1. Retrieve drugs list from NDC
  
  drugs <- getDrugsByNonProprietaryName(name)
  records <- list()
  
  # 2. Query the medline for contents similar to the colected information
  
  terms <- c(name)
  
  # 2.1. Associate aditional info from ADReCS
  res <- getDrugsByName(adresConn, name)
  
  if(length(res) < 1) {
    print("No records in ADReCS found")
    return()
  }
  
  #Create empty dataset so it can be used in rbind
  adrTerms <- data.frame(term=character())
  for(j in 1:nrow(res)) {
    #For each drug, get its known adrs
    drugAdrs <- getDrugsAdrs(adresConn, res[j,])
    adrTerms <- rbind(adrTerms, drugAdrs)
  }
  
  if(nrow(adrTerms) > 0){
    terms <- adrTerms[,1]
    
    #2.2 Query medline with terms    
    pmids <- getInterestingRecords(terms)
    info <- getSelectedRecordsInfo(pmids)
    
    # save the collected info
    rec <- list(terms, info)
    records[[length(records) + 1]] <- rec
    
    filename <- paste(c("record_", name, ".R"), collapse="")
    save(records, file=filename)
    print("Saved record to file ", filename)

    return()
  }
}

analyseData <- function(name) {
  filename <- paste(c("record_", name, ".R"), collapse="")
  
  # 3. Gather differences of slope between the before after entry in market approximate lines
  for(i in 1:length(records)) {
    # structure the nr of reports by month
    # TODO (check data type)
    
    
    # drug.lm = lm(date ~ nrReports, data=rec) 
    # coeffs = coefficients(drug.lm); coeffs[2]
  }
}



##
## Cleanup
##
clean <- function() {
  dbDisconnect(medlineConn)
  dbDisconnect(adresConn)
  dbDisconnect(ndcConn)
}
