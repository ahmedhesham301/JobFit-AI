CREATE TYPE status AS ENUM (
    'unfiltered',
    'bad_fit',
    'good_fit_sent',
    'good_fit_not_sent'
);

CREATE TABLE jobs (
    url VARCHAR PRIMARY KEY,
    title VARCHAR NOT NULL,
    description VARCHAR NOT NULL,
    percentage SMALLINT,
    status status NOT NULL DEFAULT 'unfiltered',
    company VARCHAR,
    location VARCHAR,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
