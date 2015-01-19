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
  
  # Escape quotes
  terms_str <- gsub("'", "''", terms_str)
  
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