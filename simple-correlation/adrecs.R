library(RMySQL)

query <- function(con, query, n=-1){
	res <- fetch(dbSendQuery(con,query),n=n)
	return(res)
}

getDrugSynonyms <- function(con, drugId){
	query <- paste('SELECT * FROM drug_synonym WHERE drug like "', drugId, sep="")
	query <- paste(query, '"', sep="")
	syns <- query(con, query)
	return(syns)
}

getDrugs <- function(con){
	query <- "SELECT * FROM drug"
	drugs <- query(con,query)
	return(drugs)
}

getConnection <- function(user='pcosta', password='pcosta', dbname='ADReCS', host='porto.fe.up.pt'){
	adrecsConn <- dbConnect(MySQL(), user=user, password=password, dbname=dbname, host=host)
	return(adrecsConn)
}


rs <- dbSendQuery(getConnection(), "SELECT drug.id, drug.name, drug_synonym.syn FROM drug JOIN drug_synonym ON drug.id = drug_synonym.drug")
drugs <- fetch(rs, n=-1)

head(drugs)
head(getDrugSynonyms(getConnection(), "BADD_D00002"))
head(getDrugs(getConnection()))