DROP TABLE drug;

CREATE TABLE drug (
	product_id VARCHAR(100) PRIMARY KEY,
	product_ndc VARCHAR(100), 
	product_type_name VARCHAR(100), 
	proprietary_name VARCHAR(100),
	proprietary_name_suffix VARCHAR(100),
	non_proprietary_name VARCHAR(100),
	dosage_for_name VARCHAR(100),
	route_name VARCHAR(100),
	start_marketing_date DATE,
	end_marketing_date DATE,
	marketing_category_name VARCHAR(100),
	application_number VARCHAR(100),
	labeler_name VARCHAR(100),
	substance_name VARCHAR(100),
	active_numerator_strength VARCHAR(100),
	active_ingred_unit VARCHAR(100),
	pharm_classes VARCHAR(100),
	dea_schedule VARCHAR(100)	
);