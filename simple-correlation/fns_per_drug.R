retrieveData <- function(name, full=TRUE) {
  # 1. Retrieve drugs list from NDC
  
  drugs <- getDrugsByNonProprietaryName(name)
  records <- list()
  
  # 2. Query the medline for contents similar to the colected information
  
  terms <- c(name)
  
  # 2.1. Associate aditional info from ADReCS
  res <- getDrugsByName(name)
  
  if(nrow(res) < 1) {
    print("No records in ADReCS found")
    return()
  }
  
  #Create empty dataset so it can be used in rbind
  adrTerms <- data.frame(term=character())
  for(j in 1:nrow(res)) {
    #For each drug, get its known adrs
    drugAdrs <- getDrugsAdrs(res[j,], full)
    adrTerms <- rbind(adrTerms, drugAdrs)
  }
  
  print(paste(c("Number of terms: ", nrow(adrTerms)), collapse=""))
  
  if(nrow(adrTerms) > 0){
    terms <- adrTerms[,1]
    
    #2.2 Query medline with terms    
    pmids <- getInterestingRecords(terms)
    filename <- paste(c("pmid_", name, ".R"), collapse="")
    save(pmids, file=filename)
    print(paste(collapse="", c("Saved pmids to file ", filename)))
    
    uniquePMIDs <- unique(pmids)
    nrIters <- ceiling(nrow(uniquePMIDs) / 1000000)
    info <- data.frame()
    
    for(i in 1:nrIters) {
      b <- (i - 1) * 1000000
      e <- min(i * 1000000 - 1, nrow(uniquePMIDs))
      
      if (nrow(info) == 0) {
        info <- getSelectedRecordsInfo(uniquePMIDs[b:e,])
      } else {
        info <- rbind(info, getSelectedRecordsInfo(uniquePMIDs[b:e,]))
      }
    }
    
    # save the collected info
    records <- list(terms, info)
    
    filename <- paste(c("record_", name, ".R"), collapse="")
    save(records, file=filename)
    print(paste(collapse="", c("Saved record to file ", filename)))
    
    return()
  }
}

analyseData <- function(name, graphics=FALSE) {
  filename <- paste(c("record_", name, ".R"), collapse="")
  load(filename)
  
  # Publications and date of publication
  entries <- records[[2]]
  
  dates <- as.Date(entries$date_created)
  years <- format(dates, format="%Y-%m")
  
  # Number of publications by year
  nPubYears <- table(years)
  
  tmp <- sapply(names(nPubYears), function(x) {paste(c(x, "-01"), collapse="")})
  x <- as.Date(tmp, "%Y-%m-%d")
  y <- as.vector(nPubYears)

  # Performs linear regression
  lm.out = lm(y~x)
  
  # Release Dates
  drugs <- getDrugsByNonProprietaryName(name)
  releaseDates <- format(as.Date(drugs$start_marketing_date), format="%Y-%m")
  releaseDates <- as.Date(sapply(releaseDates, function(x) {paste(c(x, "-01"), collapse="")}), "%Y-%m-%d")

  if(graphics) {
    plot(x,y)
    abline(lm.out, col="red")
    abline(v=releaseDates, col="green")
  }
}

drugHistogram <- function(n=10, full=TRUE){

  filename <- "drug_histogram.R"

  histogram <- data.frame(Drug=character(), Num=c())
  if( file.exists(filename))
    load(filename)

  # 1. Fetch n drugs from ADRECS
  drugs <- getDrugs(n=n, skip=nrow(histogram))

  # 2. For each drug d
  for(i in 1:nrow(drugs)){
    # 2.1 Get know adrs from d and add to list
    drugAdrs <- getDrugsAdrs(drugs[i,]$id, full)
    terms <- c(drugs[i,]$name,drugAdrs$term)

    # 2.2 Query medline for pmids and add to histogram
    pmids <- getInterestingRecords(terms)

    histogram <- rbind(histogram, data.frame(Drug=drugs[i,]$name, Num=nrow(unique(pmids))))
    save(histogram, file=filename)
    print(paste("Saved drug", drugs[i,]$name))
  }

  # 3. Plot histogram
  plot(histogram)
}