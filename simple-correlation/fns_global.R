library("stringr")
library("lubridate")

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
  
  filename <- paste(c("data_", as.character(Sys.Date()), ".R"), collapse="")
  
  for(record in availableRecords) {
    drugName <- str_match(record, "record_(.*).R")[1,2]
    if(is.na(drugName)) {
      next
    }
    print(paste(c("Processing ", drugName)), collapse="")
    drugResults <- analyseData(drugName)
    unname(drugResults)
    if(!is.null(drugResults) && length(drugResults) != 0) {
      regressions <- rbind(regressions, data.frame(drugName=drugName, before=drugResults[1], after=drugResults[2]))
     
      save(regressions, file=filename)
      
      msg <- paste(c("Saved current data to ", filename))
      print(msg)
    }
  }
  
  return(regressions)
}

retrieveGlobalTendency <- function() {
  
  print("Retrieving all dates from medline")
  dates <- getAllReleaseDates()
  dates[[1]] <- as.Date(dates[[1]])
  
  print("Agregating in trimesters")
  trimesters <- lapply(dates[1], function(x) {
    day(x) <- 1
    month(x) <- ((month(x) - 1) %/% 3) * 3 + 1
    x
  })
  
  dates[[1]] <- trimesters[[1]]
  
  nPubTrimester <- aggregate(count ~ date_created, FUN="sum", data=dates)
  
  plotFileName <- paste("helpers/plot_global.jpg", sep="")
  jpeg(file=plotFileName)
  plot(nPubTrimester)
  print(paste("Saved plot to", plotFileName, sep=" "))
  dev.off()
  
  return(NULL)
}