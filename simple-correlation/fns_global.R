retrieveAllData() <- function() {
  drugs <- getDistinctNDCDrugs()
  for (i in 1:nrows(drugs)) {
    retrieveData(drugs[i,])
  }
}