##
## Medline
##

getSelectedRecordsInfo <- function(pmids) {
  medlineConn <- getConnection(dbname='medline')
  qs <- c("SELECT pmid, date_created 
          FROM medline_citation 
          WHERE pmid IN (",
          paste0(pmids, collapse=","),
          ") ORDER BY date_created")
  query <- paste(qs, collapse="")
  res <- query(medlineConn, query, n=1000)
  dbDisconnect(medlineConn)
  return(res)
}

getAllRecordsInfo <- function() {
  
}

getInterestingRecords <- function(terms) {
  medlineConn <- getConnection(dbname='medline')

  #Add a minus before the drug name to exclude it from the search results
  #Removes the papers written in the research of the drug
  terms[1] <- paste0('-', terms[1], collapse="")
  terms_str <- paste0(terms, collapse="\" \"")
  
  # Escape quotes
  terms_str <- gsub("'", "''", terms_str)
  
  qs <- c("SELECT pmid
          FROM medline_citation
          WHERE MATCH(article_title, abstract_text)
          AGAINST ('\"",
          terms_str,
          "\"' IN BOOLEAN MODE)")
  query <- paste(qs, collapse="")
  
  res <- query(medlineConn, query, n=1000)
  
  qs <- c("SELECT pmid
          FROM medline_keyword_list
          WHERE MATCH(keyword)
          AGAINST ('\"",
          terms_str,
          "\"' IN BOOLEAN MODE)")
  query <- paste(qs, collapse="")
  res <- rbind(res, query(medlineConn, query, n=1000))
  
  qs <- c("SELECT pmid
          FROM medline_mesh_heading
          WHERE MATCH(descriptor_name)
          AGAINST ('\"",
          terms_str,
          "\"' IN BOOLEAN MODE)")
  query <- paste(qs, collapse="")
  res <- rbind(res, query(medlineConn, query, n=1000))
  
  qs <- c("SELECT pmid
          FROM medline_mesh_heading_qualifier
          WHERE MATCH(descriptor_name)
          AGAINST ('\"",
          terms_str,
          "\"' IN BOOLEAN MODE)")
  query <- paste(qs, collapse="")
  res <- rbind(res, query(medlineConn, query, n=1000))
  
  qs <- c("SELECT pmid
          FROM medline_citation_other_abstract
          WHERE MATCH(abstract_text)
          AGAINST ('\"",
          terms_str,
          "\"' IN BOOLEAN MODE)")
  query <- paste(qs, collapse="")
  res <- rbind(res, query(medlineConn, query, n=1000))
  
  dbDisconnect(medlineConn)
  return(res)
}

getAllReleaseDates <- function() {
  medlineConn <- getConnection(dbname='medline')
  query <- c("SELECT date_created, COUNT(*) AS count
          FROM medline_citation 
          GROUP BY date_created")
  res <- query(medlineConn, query, n=1000)
  dbDisconnect(medlineConn)
  return(res)
}

hasSelectedMesh <- function(pmids, mesh_terms){
  medlineConn <- getConnection(dbname='medline')
  pmids <- paste0(pmids, collapse=", ")
  mesh_terms <- paste0(mesh_terms, collapse=', ')
  qs <- c("SELECT medline_citation pmid
          FROM medline_citation
            INNER JOIN medline_mesh_heading
            ON medline_citation.pmid = medline_mesh_heading.pmid
          WHERE medline_citation.pmid IN (", pmids,
          ") AND medline_mesh_heading.descriptor_name IN (",
          mesh_terms, ")")
  query <- paste(qs, collapse="")
  res <- query(medlineConn, query, n=1000)
  dbDisconnect(medlineConn)
  return(res)
}

getAbstracts <- function(pmids){
  medlineConn <- getConnection(dbname='medline')
  terms <- paste0(pmids, collapse=", ")
  qs <- c("SELECT distinct(abstract_text) 
          FROM medline_citation_other_abstract 
          WHERE pmid in (", terms,
          ") AND type NOT LIKE 'Publisher'")
  query <- paste(qs, collapse="")
  res <- query(medlineConn, query, n=1000)
  dbDisconnect(medlineConn)
  return(res)
}
