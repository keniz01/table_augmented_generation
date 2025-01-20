DO $$
-- for each record in tbl_record_import
DECLARE 
	tbl_record_import_row tbl_record_import%ROWTYPE;
	album_row album%ROWTYPE;
	label_row record_label%ROWTYPE;
	genre_row genre%ROWTYPE;
	artist_row recording_artist%ROWTYPE;
BEGIN
    FOR tbl_record_import_row IN SELECT * FROM tbl_record_import LOOP

	-- if label name length greater than 0 and does not exist in record_label table
	    IF (LENGTH(tbl_record_import_row.album_label) > 0)
		AND (NOT EXISTS(SELECT 1 FROM record_label WHERE record_label.label_name IS NOT DISTINCT FROM tbl_record_import_row.album_label)) 
		THEN
	        RAISE NOTICE 'Inserting label_name: %', tbl_record_import_row.album_label;
			-- insert label name
			INSERT INTO record_label (label_name) VALUES (tbl_record_import_row.album_label);
	    END IF;
	-- if genre name length greater than 0 does not exist in genre table
	    IF (LENGTH(tbl_record_import_row.genre_name) > 0)
		AND (NOT EXISTS(SELECT 1 FROM genre WHERE genre_name IS NOT DISTINCT FROM tbl_record_import_row.genre_name)) 
		THEN
	        RAISE NOTICE 'Inserting genre_name: %', tbl_record_import_row.genre_name;
			-- insert genre name
			INSERT INTO genre (genre_name) VALUES (tbl_record_import_row.genre_name);
	    END IF;
	-- if artist name  length greater than 0 does not exist in recording_artist table
	    IF (LENGTH(tbl_record_import_row.artist_name) > 0)
		AND (NOT EXISTS(SELECT 1 FROM recording_artist WHERE artist_name IS NOT DISTINCT FROM tbl_record_import_row.artist_name)) 
		THEN
	        RAISE NOTICE 'Inserting artist_name: %', tbl_record_import_row.artist_name;
			-- insert artist_name
			INSERT INTO recording_artist (artist_name) VALUES (tbl_record_import_row.artist_name);
	    END IF;
		-- if album name length greater than 0 does not exist in album table
	    IF (LENGTH(tbl_record_import_row.album_title) > 0) THEN

			SELECT * INTO genre_row FROM genre WHERE genre_name IS NOT DISTINCT FROM tbl_record_import_row.genre_name;
			SELECT * INTO label_row FROM record_label WHERE label_name IS NOT DISTINCT FROM tbl_record_import_row.album_label;
			SELECT * INTO artist_row FROM recording_artist WHERE artist_name IS NOT DISTINCT FROM tbl_record_import_row.artist_name;

			IF (NOT EXISTS(SELECT 1 
				FROM album 
				WHERE album.title IS NOT DISTINCT FROM tbl_record_import_row.album_title
				AND genre_id IS NOT DISTINCT FROM genre_row.genre_id
				AND label_id IS NOT DISTINCT FROM label_row.label_id
				AND artist_id IS NOT DISTINCT FROM artist_row.artist_id)) 
			THEN
		        RAISE NOTICE 'Inserting album_title: %', tbl_record_import_row.album_title;
				-- insert album
				INSERT INTO album (title, genre_id, label_id, artist_id) 
				VALUES (tbl_record_import_row.album_title, genre_row.genre_id, label_row.label_id, artist_row.artist_id);					
			END IF;
		END IF;
		-- if track length greater than 0 does not exist in track table
	    IF (LENGTH(tbl_record_import_row.track_title) > 0) THEN
			SELECT * INTO genre_row FROM genre WHERE genre_name IS NOT DISTINCT FROM tbl_record_import_row.genre_name;
			SELECT * INTO label_row FROM record_label WHERE label_name IS NOT DISTINCT FROM tbl_record_import_row.album_label;
			SELECT * INTO artist_row FROM recording_artist WHERE artist_name IS NOT DISTINCT FROM tbl_record_import_row.artist_name;
			SELECT * INTO album_row FROM album WHERE title IS NOT DISTINCT FROM tbl_record_import_row.album_title;
			
			IF (NOT EXISTS(SELECT 1 
				FROM track 
				WHERE title IS NOT DISTINCT FROM tbl_record_import_row.track_title
				AND genre_id IS NOT DISTINCT FROM genre_row.genre_id
				AND label_id IS NOT DISTINCT FROM label_row.label_id
				AND artist_id IS NOT DISTINCT FROM artist_row.artist_id
				AND album_id IS NOT DISTINCT FROM album_row.album_id ))
			THEN
		        RAISE NOTICE 'Inserting track_title: %', tbl_record_import_row.track_title;
				-- insert track_title
				INSERT INTO track (title, duration, position, release_year, genre_id, label_id, artist_id, album_id) 
				VALUES (tbl_record_import_row.track_title, tbl_record_import_row.track_length, tbl_record_import_row.track_position, 
					tbl_record_import_row.track_year, genre_row.genre_id, label_row.label_id, artist_row.artist_id, album_row.album_id);
	
			END IF;
		END IF;
	END LOOP;
END $$;