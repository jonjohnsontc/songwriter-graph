-- Carrying basic data about tracks
CREATE TABLE tracks (
    track_id text primary key,
    track_name text,
    artists jsonb 
);