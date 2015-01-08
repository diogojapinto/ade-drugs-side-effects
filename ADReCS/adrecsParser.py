import xml.etree.ElementTree as ET 
import dbConnector

def escapeSqlStrings(str):
	return str.replace("'", "''")

def insertString(data, key, value):
	data[key] = "'" + escapeSqlStrings(value) + "'"

strType = 1

insertData = {
	strType: insertString
} 

def insertAdr(ADR):
	adrData = {}

	id = ADR.find('ADReCS_ID')
	term = ADR.find('ADR_TERM')
	description = ADR.find('ADR_DESCRIPTION')
	whoArt = ADR.find('WHO_ART_CODE')
	meddra = ADR.find('MEDDRA_CODE')

	insertData[strType](adrData, 'who_art_code', whoArt.text)
	insertData[strType](adrData, 'description', description.text)
	insertData[strType](adrData, 'term', term.text)
	insertData[strType](adrData, 'id', id.text)
	insertData[strType](adrData, 'meddra', meddra.text)

	dbConnector.insertInto(dbConnector.ADR, adrData)

	return id.text

def insertSynonyms(synonyms, id, idField, table):
	#Has childs
	if len(synonyms) > 0:
		for synonym in synonyms:
			if synonym.text:
				synonymData = {}
				insertData[strType](synonymData,'syn', synonym.text)
				insertData[strType](synonymData,idField, id)
				dbConnector.insertInto(table, synonymData)
	elif synonyms.text != "Not Available":
		synonymData = {}
		insertData[strType](synonymData,'syn', synonyms.text)
		insertData[strType](synonymData,idField, id)
		dbConnector.insertInto(table, synonymData)

def insertAdrDrugs(ADR, adrId):
	drugs = ADR.find('Drugs')
	for Drug in drugs:
		drugData={}

		drugId = Drug.find('DRUG_ID')
		drugName = Drug.find('DRUG_NAME')

		insertData[strType](drugData,'adr_id', adrId)
		insertData[strType](drugData,'drug_id', drugId.text)

		dbConnector.insertInto(dbConnector.DRUG_ADR, drugData)

def insertDrug(Drug):
	drugData = {}

	drugId = Drug.find('DRUG_ID')
	name = Drug.find('DRUG_NAME')
	description = Drug.find('DESCRIPTION')
	atc = Drug.find('ATC')
	indications = Drug.find('INDICATIONS')
	cas = Drug.find('CAS')

	insertData[strType](drugData,'id', drugId.text)
	insertData[strType](drugData,'name', name.text)
	insertData[strType](drugData,'description', description.text)
	insertData[strType](drugData,'atc', atc.text)
	insertData[strType](drugData,'indications', indications.text)
	insertData[strType](drugData,'cas', cas.text)

	dbConnector.insertInto(dbConnector.DRUG, drugData)

	return drugId.text
	
def insertAdrRelatedToDrug(Drug, drugId):
	adrs = Drug.find('ADRs')

	for adr in adrs:
		adrDrugData = {}

		adrId = adr.find('ADRECS_ID')
		frequency = adr.find('FREQUENCY')

		insertData[strType](adrDrugData,'drug_id', drugId)
		insertData[strType](adrDrugData,'adr_id', adrId.text)
		insertData[strType](adrDrugData,'frequency', frequency.text)

		dbConnector.insertInto(dbConnector.DRUG_ADR, adrDrugData)

########################################################################
#                              SCRIPT INIT                             #
########################################################################

adrTree = ET.parse('ADReCS_ADR_info.xml')
adrRoot = adrTree.getroot()

drugTree = ET.parse('ADReCS_Drug_info.xml')
drugRoot = drugTree.getroot()

recordsInserted = 0

dbConnector.useDatabase()


dbConnector.initDatabase()

for ADR in adrRoot:
	adrId = insertAdr(ADR)
	synonyms = ADR.find('ADR_SYNONYMS')
	insertSynonyms(synonyms,adrId, 'adr', dbConnector.ADR_SYNONYM)

	recordsInserted+=1
	print("ADR with id", adrId, "inserted. Inserted", recordsInserted, "records")

dbConnector.commit()

for Drug in drugRoot:
	drugId = insertDrug(Drug)
	synonyms = Drug.find('DRUG_SYNONYMS')
	insertSynonyms(synonyms, drugId, 'drug', dbConnector.DRUG_SYNONYM)

	insertAdrRelatedToDrug(Drug, drugId)

	recordsInserted+=1
	print("Drug with id", drugId, "inserted. Inserted", recordsInserted, "records")

dbConnector.commit()

for ADR in adrRoot:
	adrId = ADR.find('ADReCS_ID').text
	insertAdrDrugs(ADR,adrId)
	print("Tried to insert drugs that lead to ADR with id", adrId)

dbConnector.close()