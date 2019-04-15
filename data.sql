DROP TABLE IF EXISTS url_data_store;

CREATE TABLE url_data_store(
 id SERIAL PRIMARY KEY,
 url_hash VARCHAR (20) NOT NULL,
 url VARCHAR (300) NOT NULL,
 created_on TIMESTAMP NOT NULL,
 viewed INT NOT NULL CHECK (viewed >= 0),
 "user" INT references users(ID),
 ip_address INET,
 deleted BOOLEAN
);

DROP TABLE IF EXISTS users;

CREATE TABLE users(
 id SERIAL PRIMARY KEY,
 username VARCHAR (100) NOT NULL,
 password VARCHAR (100) NOT NULL,
 email VARCHAR (70) NOT NULL UNIQUE,
 created_on TIMESTAMP NOT NULL,
 updated_on TIMESTAMP NOT NULL,
 deleted BOOLEAN
);

INSERT INTO users (username, password, email, created_on, updated_on, deleted)
VALUES ('DeepBlack', 'hash_string', 'andrew@dorokhin.moscow', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, false);

ALTER TABLE url_data_store ADD COLUMN deleted BOOLEAN;
ALTER TABLE url_data_store ALTER COLUMN deleted SET DEFAULT FALSE;

CREATE INDEX ON url_data_store USING gist (ip_address inet_ops);
CREATE INDEX ON url_data_store(url_id);
CREATE UNIQUE INDEX users_unique_lower_email_idx ON users (lower(email));

INSERT INTO url_data_store (url, url_hash, created_on, viewed, ip_address)
VALUES ('habr.com', 'TesT_stringHasH223', CURRENT_TIMESTAMP,  0, '44.75.21.76');


select * from url_data_store;

UPDATE url_data_store SET deleted = TRUE WHERE url_id between 2 and 5;

select count(*) from users WHERE email ~ '\ygoogle\y';
