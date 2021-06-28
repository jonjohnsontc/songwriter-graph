CREATE TABLE api_categories (
    id serial,
    pull_timestamp timestamp DEFAULT current_timestamp,
    data jsonb
);