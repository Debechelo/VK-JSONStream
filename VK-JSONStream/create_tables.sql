CREATE TABLE applications (
    id SERIAL PRIMARY KEY,
    kind VARCHAR(32) NOT NULL,
    name VARCHAR(128) NOT NULL,
    description TEXT NOT NULL,
    version VARCHAR(255) NOT NULL,
    configuration JSONB NOT NULL,
    settings JSONB,
    state VARCHAR(255),
);