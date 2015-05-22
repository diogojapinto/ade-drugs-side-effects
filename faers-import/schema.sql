DROP TABLE IF EXISTS event_indications;
DROP TABLE IF EXISTS event_therapy;
DROP TABLE IF EXISTS event_report_sources;
DROP TABLE IF EXISTS event_outcomes;
DROP TABLE IF EXISTS event_reactions;
DROP TABLE IF EXISTS event_drugs;
DROP TABLE IF EXISTS event;


CREATE TABLE event (
	primaryid			INTEGER NOT NULL,
	caseid				INTEGER NOT NULL,
	caseversion			VARCHAR(100),
	i_f_code			CHAR(1),
	event_dt 			DATE,
	mfr_dt				DATE,
	init_fda_dt			DATE,
	fda_dt 				DATE,
	rept_cod			CHAR(3),
	auth_num			INTEGER,
	mfr_num				INTEGER,
	mfr_sndr			VARCHAR(100),
	lit_ref				VARCHAR(500),
	age 				INTEGER,
	age_cod				CHAR(3),
	age_grp				CHAR(1),
	sex					CHAR(1),
	e_sub				CHAR(1),
	wt					FLOAT,
	wt_cod				CHAR(3),
	rept_dt				DATE,
	to_mfr				BOOLEAN,
	occp_cod			CHAR(3),
	reporter_country	CHAR(2),
	occr_country		CHAR(2)
);
CREATE UNIQUE INDEX pk_faers_event ON event(primaryid);
ALTER TABLE event
	ADD CONSTRAINT pk_faers_event PRIMARY KEY (primaryid);


CREATE TABLE event_drugs (
	primaryid			INTEGER NOT NULL,
	caseid				INTEGER NOT NULL,
	drug_seq			INTEGER,
	role_cod			CHAR(2),
	drugname			VARCHAR(100),
	prod_ai				VARCHAR(100),
	val_vbm				CHAR(1),
	route				VARCHAR(100),
	dose_vbm			VARCHAR(500),
	cum_dose_chr		FLOAT,
	cum_dose_unit		CHAR(10),
	dechal				CHAR(1),
	rechal				CHAR(1),
	lot_num				VARCHAR(50),
	exp_dt				DATE,
	nda_num				INTEGER,
	dose_amt			FLOAT,
	dose_unit 			CHAR(10),
	dose_form			VARCHAR(50),
	dose_freq			CHAR(3)
);
CREATE INDEX idx_event_drugs_primaryid ON event_drugs(primaryid);

CREATE TABLE event_reactions (
	primaryid			INTEGER NOT NULL,
	caseid				INTEGER,
	medra_pt 			VARCHAR(500),
	drug_rec_act		VARCHAR(500)
);
CREATE INDEX idx_event_reactions_primaryid ON event_reactions(primaryid);

CREATE TABLE event_outcomes (
	primaryid			INTEGER NOT NULL,
	caseid				INTEGER,
	outc_cod			CHAR(2)
);
CREATE INDEX idx_event_outcomes_primaryid ON event_outcomes(primaryid);

CREATE TABLE event_report_sources (
	primaryid			INTEGER NOT NULL,
	caseid				INTEGER,
	rpsr_cod			CHAR(3)
);
CREATE INDEX idx_event_report_sources_primaryid ON event_report_sources(primaryid);

CREATE TABLE event_therapy (
	primaryid			INTEGER NOT NULL,
	caseid				INTEGER,
	dsg_drug_seq		INTEGER,
	start_dt			DATE,
	end_dt				DATE,
	dur 				INTEGER,
	dur_cod				CHAR(3)
);
CREATE INDEX idx_event_therapy_primaryid ON event_therapy(primaryid);

CREATE TABLE event_indications (
	primaryid			INTEGER NOT NULL,
	caseid 				INTEGER,
	indi_drug_seq		INTEGER,
	medra_indi_pt		VARCHAR(500)
);
CREATE INDEX idx_event_indications_primaryid ON event_indications(primaryid);
