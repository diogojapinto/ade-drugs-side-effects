library(RMySQL)

adrecsConn <- dbConnect(MySQL(), user='pcosta', password='pcosta', dbname='ADReCS', host='porto.fe.up.pt')

rs <- dbSendQuery(adrecsConn, "SELECT drug.id, drug.name, drug_synonym.syn FROM drug JOIN drug_synonym ON drug.id = drug_synonym.drug")
drugs <- fetch(rs, n=-1)

head(drugs)