-- music.database_meta_data definition

-- Drop table

-- DROP TABLE music.database_meta_data;

CREATE TABLE music.database_meta_data (
	table_schema_id int4 GENERATED ALWAYS AS IDENTITY NOT NULL, -- Table schema id
	table_name varchar NOT NULL, -- The table name
	table_description varchar NOT NULL, -- The table description
	table_json_schema jsonb NOT NULL, -- The json string of the table schema
	vector_embeddings music.vector(384) NOT NULL, -- The table schema json string embeddings
	CONSTRAINT database_meta_data_pk PRIMARY KEY (table_schema_id),
	CONSTRAINT database_meta_data_table_name_unique UNIQUE (table_name),
	CONSTRAINT database_meta_data_table_json_schema_unique UNIQUE (table_json_schema)
);

-- Column comments

COMMENT ON COLUMN music.database_meta_data.table_schema_id IS 'Table schema id';
COMMENT ON COLUMN music.database_meta_data.table_name IS 'The table name';
COMMENT ON COLUMN music.database_meta_data.table_description IS 'The table description';
COMMENT ON COLUMN music.database_meta_data.table_json_schema IS 'The json string of the table schema';
COMMENT ON COLUMN music.database_meta_data.vector_embeddings IS 'The table schema json string embeddings';