library("stringr")

retrieveAllData <- function() {
  drugs <- getDistinctNDCDrugs()
  for (i in 1:nrow(drugs)) {
    print(paste(collapse="", c("Processing ", drugs[i,], "...")))
    retrieveData(drugs[i,])
    print("Finished")
  }
}

analyseAllData <- function() {
  
  availableRecords <- list.files("records/")
  
  regressions <- data.frame(drugName=character(0), before=numeric(0), after=numeric(0), stringsAsFactors=FALSE)
  
  for(record in availableRecords) {
    drugName <- str_match(record, "record_(.*).R")[1,2]
    if(is.na(drugName)) {
      next
    }
    print(paste(c("Processing ", drugName)), collapse="")
    drugResults <- analyseData(drugName)
    unname(drugResults)
    if(!is.null(drugResults) && length(drugResults) != 0) {
      regressions <- rbind(regressions, data.frame(drugName, drugResults[1], drugResults[2]))
    }
  }
  
  filename <- paste(c("data_", as.character(Sys.Date()), ".R"), collapse="")
  save(regressions, file=filename)
  
  msg <- paste(c("Saved current data to ", filename))
  print(msg)
  
  return(regressions)
}