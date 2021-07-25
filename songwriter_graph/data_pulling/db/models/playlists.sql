-- designed to carry the primary details about spotify playlists
-- so that their associated tracks can be pulled
CREATE TABLE playlists (
    id serial primary key,
    playlist_id text,
    snapshot_id text,
    playlist_name text,
    uri text,
    pull_timestamp timestamp DEFAULT current_timestamp
);