# retrieveData <- function(name, full=TRUE) {
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
  
  if(nrow(adrTerms) > 0){
    terms <- adrTerms[,1]
    
    #2.2 Query medline with terms    
    pmids <- getInterestingRecords(terms)
    filename <- paste(c("pmids/pmid_", name, ".R"), collapse="")
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
    
    filename <- paste(c("records/record_", name, ".R"), collapse="")
    save(records, file=filename)
    print(paste(collapse="", c("Saved record to file ", filename)))
    
    return()
  }
}

analyseData <- function(name) {
  filename <- paste(c("records/record_", name, ".R"), collapse="")
  load(filename)
  
  # Publications and date of publication
  entries <- records[[2]]
  
  if(sum(!is.na(entries)) == 0) {
    print("No records found")
    return(NULL)
  }
  
  dates <- as.Date(entries$date_created)
  
  # Limit dates to 1990-2013
  valid.dates <- dates >= as.Date("1990-01-01") & dates <= as.Date("2013-12-31")
  dates <- dates[valid.dates]
  years <- format(dates, format="%Y-%m")
  
  # Number of publications by year
  nPubYears <- table(years)
  
  tmp <- sapply(names(nPubYears), function(x) {paste(c(x, "-01"), collapse="")})
  x <- as.Date(tmp, "%Y-%m-%d")
  y <- as.vector(nPubYears)
  
  # Release Dates
  drugs <- getDrugsByNonProprietaryName(name)
  releaseDates <- format(as.Date(drugs$start_marketing_date), format="%Y-%m")
  releaseDates <- as.Date(sapply(releaseDates, function(x) {paste(c(x, "-01"), collapse="")}), "%Y-%m-%d")

  beforeIdx = which(x < min(releaseDates))
  
  if(length(beforeIdx) == 0 || length(beforeIdx) == length(x)) {
    print("Not enough data to compare")
    return(NULL)
  }

  # Performs linear regression
  lm.before = lm(y[beforeIdx]~x[beforeIdx])
  lm.after = lm(y[-beforeIdx]~x[-beforeIdx])
  
  # Save plot to file
  plotFileName <- paste("plots/plot_", name, ".jpg", sep="")
  jpeg(file=plotFileName)
  plot(x,y)
  abline(lm.before, col="red")
  abline(lm.after, col="blue")
  abline(v=releaseDates, col="green")
  print(paste("Saved plot to", plotFileName, sep=" "))
  dev.off()
  return(c(coef(lm.before)[2], coef(lm.after)[2]))
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