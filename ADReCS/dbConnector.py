import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'ADReCS'

ADR = "adr";
ADR_SYNONYM = "adr_synonym"
DRUG = "drug"
DRUG_ADR = "drug_adr"
DRUG_SYNONYM = "drug_synonym"

TABLES = []
TABLES.append(
	"CREATE TABLE " + ADR +" ("  
	"  id varchar(13) PRIMARY KEY,"
	"  term varchar(60) NOT NULL,"
	"  description varchar(60),"
	"  who_art_code varchar(14),"
	"  meddra varchar(14)"
	")"
)
TABLES.append(
	"CREATE TABLE " + ADR_SYNONYM + " ("  
	"  syn varchar(60),"
	"  adr varchar(13),"
	"  PRIMARY KEY (syn, adr),"
	"  FOREIGN KEY (adr) REFERENCES " + ADR + "(id))"
)
TABLES.append(
	"CREATE TABLE " + DRUG + " ("  
	"  id varchar(12) PRIMARY KEY,"
	"  name varchar(60),"
	"  description varchar(1000),"
	"  atc varchar(8),"
	"  indications varchar(600),"
	"  cas varchar(14)"
	")"
)
TABLES.append(
	"CREATE TABLE " + DRUG_ADR + " ("  
	"  adr_id varchar(13),"
	"  drug_id varchar(12),"
	"  frequency varchar(5),"
	"  PRIMARY KEY (adr_id, drug_id),"
	"  FOREIGN KEY (adr_id) REFERENCES " + ADR + "(id),"
	"  FOREIGN KEY (drug_id) REFERENCES "+ DRUG + "(id))"
)
TABLES.append(
	"CREATE TABLE " + DRUG_SYNONYM + " ("  
	"  syn varchar(60),"
	"  drug varchar(12),"
	"  PRIMARY KEY (syn, drug),"
	"  FOREIGN KEY (drug) REFERENCES " + DRUG + "(id))"
)

DATABASE = []
DATABASE.append(
	"DROP DATABASE IF EXISTS " + DB_NAME
)
DATABASE.append(
	"CREATE DATABASE IF NOT EXISTS " + DB_NAME
)


cnx = mysql.connector.connect(user='pcosta', password='pcosta', host='porto.fe.up.pt')
cursor = cnx.cursor()

def executeCommands(commandList):
	for ddl in commandList:
		cursor.execute(ddl)

def recreateDatabase():
	executeCommands(DATABASE)

def createTables():
	executeCommands(TABLES)

def useDatabase():
	cnx.database = DB_NAME

def initDatabase():
	recreateDatabase()
	useDatabase()
	createTables()

duplicates = 0

def insertInto(table, data):
	firstPart = ("INSERT INTO " + table + " ( ")
	secondPart = "VALUES ( "

	for attribute, value in data.items():
		firstPart+= attribute + ", "
		secondPart+= value + ", "

	firstPart = firstPart[:-2] + ")"
	secondPart= secondPart[:-2]+ ")"

	insert = firstPart + " " + secondPart

	try:
		cursor.execute(insert)
	except mysql.connector.errors.IntegrityError:
		global duplicates
		duplicates+=1
		print("Found", duplicates, "duplicates")
	

def commit():
	cnx.commit()

def close():
	cnx.commit()
	cursor.close()
	cnx.close()