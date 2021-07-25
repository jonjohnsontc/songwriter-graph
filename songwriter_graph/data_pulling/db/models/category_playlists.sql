CREATE TABLE api_category_playlists (
    id serial,
    pull_timestamp timestamp DEFAULT current_timestamp,
    data_ jsonb
);