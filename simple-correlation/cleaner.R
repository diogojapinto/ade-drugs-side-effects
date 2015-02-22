library("iterators")
library("parallel")
library("foreach")
library("doParallel")

##
## Retrieves the popular PMID's. that shall be removed from the samples before analyseData is ran on them
##
getPopularPMIDs <- function(threshold) {
  
  if (file.exists("helpers/popular_pmids.R")) {
    load("helpers/popular_pmids.R")
  } else {
    pmids <- loadPMIDsCount()
  }
  
  selection <- pmids$count >= threshold
  return(pmids[selection,])
}

##
## For each pmid, retrieves the number of documents it appears in
##
loadPMIDsCount <- function() {
  
  # make cluster
  cl <- makeCluster(detectCores() - 1)
  registerDoParallel(cl, cores = detectCores() - 1)
  
  availableRecords <- list.files("records/")
  nr_drugs <- length(availableRecords)
  pmids <- data.frame(pmids=character(0), count=numeric(0))
  
  # do parallel computation
  pmids = foreach(record = availableRecords, .packages=c(), .combine=rbind) %dopar% {
    try({
      print(paste("Processing", record))
      load(paste(c("records/", record), collapse=""))
      new_pmids = records[[2]][[1]]
      
      data.frame(pmids=new_pmids, count=rep_len(1, length(new_pmids)))
    })
  }
  
  stopCluster(cl)
  
  print("aggregating...")
  pmids <- aggregate(count ~ pmids, FUN="sum", data=pmids)
  
  filename <- "helpers/popular_pmids.R"
  save(pmids, file=filename)
  
  return(pmids)
}