SELECT 
	tbl.table_schema, 
	tbl.table_name, 
	pgd_tbl.description table_description, 
	cols.column_name, 
	cols.data_type column_data_type, 
	cols.is_nullable is_column_nullable, 
	pgd_col.description column_description, 
	tc.constraint_type column_constraint_type
FROM information_schema.tables tbl
JOIN information_schema.columns cols ON cols.table_name = tbl.table_name
LEFT join information_schema.key_column_usage kcu on kcu.table_name = cols.table_name and kcu.column_name = cols.column_name
LEFT join information_schema.table_constraints tc on tc.table_name = cols.table_name and tc.constraint_name = kcu.constraint_name
JOIN pg_catalog.pg_namespace pgn ON pgn.nspname=tbl.table_schema
JOIN pg_catalog.pg_class pgc ON pgc.relname = tbl.table_name AND pgc.relnamespace=pgn.oid
JOIN pg_catalog.pg_description pgd_col ON pgd_col.objsubid = cols.ordinal_position AND pgd_col.objoid=pgc.oid
LEFT JOIN pg_catalog.pg_description pgd_tbl ON pgd_tbl.objsubid = 0 AND pgd_tbl.objoid=pgc.oid
WHERE tbl.table_schema='music' and tbl.table_name <> 'database_meta_data' 
ORDER BY tbl.table_schema, tbl.table_name, cols.column_name