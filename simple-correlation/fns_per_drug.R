retrieveData <- function(name, full=TRUE) {
  # 1. Retrieve drugs list from NDC
  
  drugs <- getDrugsByNonProprietaryName(name)
  records <- list()
  
  # 2. Query the medline for contents similar to the colected information
  
  terms <- c(name)
  
  # 2.1. Associate aditional info from ADReCS
  res <- getDrugsByName(adresConn, name)
  
  if(nrow(res) < 1) {
    print("No records in ADReCS found")
    return()
  }
  
  #Create empty dataset so it can be used in rbind
  adrTerms <- data.frame(term=character())
  for(j in 1:nrow(res)) {
    #For each drug, get its known adrs
    drugAdrs <- getDrugsAdrs(adresConn, res[j,], full)
    adrTerms <- rbind(adrTerms, drugAdrs)
  }
  
  print(paste(c("Number of terms: ", nrow(adrTerms)), collapse=""))
  
  if(nrow(adrTerms) > 0){
    terms <- adrTerms[,1]
    
    #2.2 Query medline with terms    
    print("Before")
    print(paste(collapse="", "Get PMIDS: ", system.time(pmids <- getInterestingRecords(terms))))
    print("Middle")
    print(paste(collapse="", "Get Dates: ", system.time(info <- getSelectedRecordsInfo(pmids))))
    print("After")
    
    # save the collected info
    records <- list(terms, info)
    
    filename <- paste(c("record_", name, ".R"), collapse="")
    save(records, file=filename)
    print("Saved record to file ", filename)
    
    return()
  }
}

analyseData <- function(name, graphics=FALSE) {
  filename <- paste(c("record_", name, ".R"), collapse="")
  load(filename)
  
  # Publications and date of publication
  entries <- records[[2]]
  
  dates <- as.Date(entries$date_created)
  years <- format(dates, format="%Y/%m")
  
  # Number of publications by year
  nPubYears <- table(years)
  
  x <- names(nPubYears)
  y <- as.vector(nPubYears)

  if(graphics) {
    plot(x,y)
  }
}