-- app/db/migrations/001_create_leads.sql

CREATE TABLE leads (
    id          SERIAL          PRIMARY KEY,
    name        VARCHAR(200)    NOT NULL,
    email       VARCHAR(200)    NOT NULL UNIQUE,
    phone       VARCHAR(50),
    message     TEXT            DEFAULT '',
    source      VARCHAR(100)    DEFAULT 'website',
    created_at  TIMESTAMP       DEFAULT NOW()
);