DROP TABLE IF EXISTS event_indications;
DROP TABLE IF EXISTS event_therapy;
DROP TABLE IF EXISTS event_report_sources;
DROP TABLE IF EXISTS event_outcomes;
DROP TABLE IF EXISTS event_reactions;
DROP TABLE IF EXISTS event_drugs;
DROP TABLE IF EXISTS event;


CREATE TABLE event (
	event_id			INTEGER NOT NULL,
	case_id				INTEGER NOT NULL,
	case_version		VARCHAR(100),
	i_f_cod				CHAR(1),
	event_dt 			DATE,
	mfr_dt				DATE,
	init_fda_dt			DATE,
	fda_dt 				DATE,
	rept_cod			CHAR(3),
	auth_num			INTEGER,
	mfr_num				INTEGER,
	mfr_sndr			VARCHAR(100),
	lift_ref			VARCHAR(500),
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
CREATE UNIQUE INDEX pk_faers_event ON event(event_id);
ALTER TABLE event
	ADD CONSTRAINT pk_faers_event PRIMARY KEY (event_id);


CREATE TABLE event_drugs (
	event_id			INTEGER NOT NULL,
	case_id				INTEGER NOT NULL,
	drug_seq			INTEGER NOT NULL,
	role_cod			CHAR(2),
	drug_name			VARCHAR(100),
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
CREATE INDEX idx_event_drugs_event_id ON event_drugs(event_id);
ALTER TABLE event_drugs
	ADD CONSTRAINT fk_event_drugs
		FOREIGN KEY event_drugs(event_id)
			REFERENCES event(event_id);
ALTER TABLE event_drugs
	ADD CONSTRAINT fk_event_drugs
		UNIQUE event_drugs(case_id, drug_seq);

CREATE TABLE event_reactions (
	event_id			INTEGER NOT NULL,
	case_id				INTEGER NOT NULL,
	medra_pt 			VARCHAR(500),
	drug_rec_act		VARCHAR(500)
);
CREATE INDEX idx_event_reactions_event_id ON event_reactions(event_id);
ALTER TABLE event_reactions
	ADD CONSTRAINT fk_event_reactions
		FOREIGN KEY event_reactions(event_id)
			REFERENCES event(event_id);


CREATE TABLE event_outcomes (
	event_id			INTEGER NOT NULL,
	case_id				INTEGER NOT NULL,
	outc_cod			CHAR(2)
		-- DE -> Death
		-- LT -> Life-Threatening
		-- HO -> Hospitalization - Initial or Prolonged
		-- DS -> Disability
		-- CA -> Congenital Anomaly
		-- RI -> Required Intervention to Prevent Permanent Impairment/Damage
		-- OT -> Other Serious (Important Medical Event)
);
CREATE INDEX idx_event_outcomes_event_id ON event_outcomes(event_id);
ALTER TABLE event_outcomes
	ADD CONSTRAINT fk_event_outcomes
		FOREIGN KEY event_outcomes(event_id)
			REFERENCES event(event_id);


CREATE TABLE event_report_sources (
	event_id			INTEGER NOT NULL,
	case_id				INTEGER NOT NULL,
	rpsr_cod			CHAR(3)
);
CREATE INDEX idx_event_report_sources_event_id ON event_report_sources(event_id);
ALTER TABLE event_report_sources
	ADD CONSTRAINT fk_event_report_sources
		FOREIGN KEY event_report_sources(event_id)
			REFERENCES event(event_id);

CREATE TABLE event_therapy (
	event_id			INTEGER NOT NULL,
	case_id				INTEGER NOT NULL,
	dsg_drug_seq		INTEGER NOT NULL,
	start_dt			DATE,
	end_dt				DATE,
	dur 				INTEGER,
	dur_cod				CHAR(3)
);
CREATE INDEX idx_event_therapy_event_id ON event_therapy(event_id);
ALTER TABLE event_therapy
	ADD CONSTRAINT fk_event_therapy
		FOREIGN KEY event_therapy(event_id)
			REFERENCES event(event_id);
ALTER TABLE event_therapy
	ADD CONSTRAINT fk_event_therapy
		UNIQUE event_therapy(case_id, dsg_drug_seq);

CREATE TABLE event_indications (
	event_id			INTEGER NOT NULL,
	case_id 			INTEGER NOT NULL,
	indi_drug_seq		INTEGER NOT NULL,
	medra_indi_pt		VARCHAR(500)
);
CREATE INDEX idx_event_indications_event_id ON event_indications(event_id);
ALTER TABLE event_indications
	ADD CONSTRAINT fk_event_indications
		FOREIGN KEY event_indications(event_id)
			REFERENCES event(event_id);
ALTER TABLE event_indications
	ADD CONSTRAINT fk_event_indications
		UNIQUE event_indications(case_id, indi_drug_seq);
