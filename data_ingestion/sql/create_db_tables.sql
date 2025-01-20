DROP TABLE IF EXISTS record_label CASCADE;
CREATE TABLE record_label (
	label_id int4 PRIMARY KEY GENERATED ALWAYS AS IDENTITY NOT NULL, -- Unique ID for each label
	label_name varchar(255) NULL UNIQUE -- Name of label
);
COMMENT ON TABLE "record_label" IS 'The record_label table maintains the record label data';
COMMENT ON COLUMN "record_label".label_id IS 'The label_id column contains the record_label table primary key';
COMMENT ON COLUMN "record_label".label_name IS 'The label_name column contains the label name';

DROP TABLE IF EXISTS recording_artist CASCADE;
CREATE TABLE recording_artist (
	artist_id int4 PRIMARY KEY GENERATED ALWAYS AS IDENTITY NOT NULL, -- Unique ID for each artist
	artist_name varchar(255) NULL UNIQUE -- Name or title of artist
);
COMMENT ON TABLE "recording_artist" IS 'The recording_artist table maintains recording artist data';
COMMENT ON COLUMN "recording_artist".artist_id IS 'The artist_id column contains the recording_artist table primary key';
COMMENT ON COLUMN "recording_artist".artist_name IS 'The artist_name columns contains recording artist name';

DROP TABLE IF EXISTS genre CASCADE;
CREATE TABLE genre (
	genre_id int4 PRIMARY KEY GENERATED ALWAYS AS IDENTITY NOT NULL, -- Unique ID for each genre
	genre_name varchar(255) NOT NULL UNIQUE -- Name of genre
);
COMMENT ON TABLE "genre" IS 'The genre table maintains the genre data';
COMMENT ON COLUMN "genre".genre_id IS 'The genre_id column contains the primary key for the genre table';
COMMENT ON COLUMN "genre".genre_name IS 'The genre_name column contains the genre name';

DROP TABLE IF EXISTS album CASCADE;
CREATE TABLE album (
	album_id int4 PRIMARY KEY GENERATED ALWAYS AS IDENTITY NOT NULL, -- Unique ID for each album
	title varchar(255) NULL, -- Name or title of album
	duration varchar(10) NULL, -- Duration or length of album 
	total_tracks int4 NULL, -- Total number of tracks on album 
	release_year int4 NULL, -- Year album was released
	genre_id int4 NULL REFERENCES genre(genre_id),  -- ID of genre for album 
	label_id int4 NULL REFERENCES record_label(label_id), -- ID of label for album 
	artist_id int4 NULL REFERENCES recording_artist(artist_id) -- ID of artist for album 
);
COMMENT ON TABLE "album" IS 'The album table maintains the album data';
COMMENT ON COLUMN "album".album_id IS 'The album_id column contains the primary key for the album table';
COMMENT ON COLUMN "album".title IS 'The title column contains the name of the album';
COMMENT ON COLUMN "album".duration IS 'The duration column contains the time it takes an album to complete playing';
COMMENT ON COLUMN "album".total_tracks IS 'The total_tracks column contains number of tracks on the album';
COMMENT ON COLUMN "album".release_year IS 'The release_year column contains the year the album was released';
COMMENT ON COLUMN "album".genre_id IS 'The genre_id column maintains a reference to the genre.genre_id column';
COMMENT ON COLUMN "album".artist_id IS 'The artist_id column maintains a reference to the artist.artist_id column';
COMMENT ON COLUMN "album".label_id IS 'The label_id column maintains a reference to the record_label.label_id column';

DROP TABLE IF EXISTS track CASCADE;
CREATE TABLE track (
	track_id int4 PRIMARY KEY GENERATED ALWAYS AS IDENTITY NOT NULL, -- Unique ID for each track
	title varchar(255) NULL, -- Name or title of track
	duration varchar(10) NULL, -- Duration or length of track 
	position int4 NULL, -- position of track on album
	release_year int4 NULL, -- year track was released
	genre_id int4 NULL REFERENCES genre(genre_id), -- ID of genre
	label_id int4 NULL REFERENCES record_label(label_id), -- ID of label
	artist_id int4 NULL REFERENCES recording_artist(artist_id), -- ID of artist
	album_id int4 NULL REFERENCES album(album_id) -- ID of album
);
COMMENT ON TABLE "track" IS 'The track table maintains the track data';
COMMENT ON COLUMN "track".track_id IS 'The track_id column contains the primary key for the track table';
COMMENT ON COLUMN "track".title IS 'The title column contains the name of the track';
COMMENT ON COLUMN "track".duration IS 'The duration column contains the time it takes a track to complete playing';
COMMENT ON COLUMN "track".position IS 'The position column contains the position on the album the track is located';
COMMENT ON COLUMN "track".release_year IS 'The release_year column contains the year the track was released';
COMMENT ON COLUMN "track".genre_id IS 'The genre_id column maintains a reference to the genre.genre_id column';
COMMENT ON COLUMN "track".artist_id IS 'The artist_id column maintains a reference to the artist.artist_id column';
COMMENT ON COLUMN "track".label_id IS 'The label_id column maintains a reference to the record_label.label_id column';
COMMENT ON COLUMN "track".album_id IS 'The album_id column maintains a reference to the album.album_id column';