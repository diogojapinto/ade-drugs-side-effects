##
## Necessary libraries
##
library("iterators")
library("parallel")
library("foreach")
library("doParallel")
library("RTextTools")
library("SparseM")
library("topicmodels")

##
## Set the working directory correctly
##

script.dir <- dirname(sys.frame(1)$ofile)
setwd(script.dir)

##
## Load additional files
##

source("mysql_con.R")
source("adrecs_lib.R")
source("ndc_lib.R")
source("medline_lib.R")
source("fns_per_drug.R")
source("fns_global.R")
source("cleaner.R")

# retrieveData('pravastatin')
