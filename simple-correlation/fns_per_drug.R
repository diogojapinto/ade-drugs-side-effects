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
    records <- list(terms, info)
    
    filename <- paste(c("record_", name, ".R"), collapse="")
    save(records, file=filename)
    print("Saved record to file ", filename)
    
    return()
  }
}

analyseData <- function(name) {
  filename <- paste(c("record_", name, ".R"), collapse="")
  load(filename)
  
  # Publications and date of publication
  entries <- records[[2]]
  
  dates <- as.Date(entries$date_created)
  years <- format(dates, format="%Y/%m")
  
  # Number of publications by year
  nPubYears <- table(years)
  plot(nPubYears)
}