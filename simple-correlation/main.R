##
## Set the working directory correctly
##

script.dir <- dirname(sys.frame(1)$ofile)
setwd(script.dir)

##
## Load additional filess
##

source("mysql_con.R")
source("adrecs_lib.R")
source("ndc_lib.R")
source("medline_lib.R")
source("fns_per_drug.R")
source("fns_global.R")

# retrieveData('pravastatin')
