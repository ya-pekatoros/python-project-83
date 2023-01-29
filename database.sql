DROP TABLE IF EXISTS urls, url_checks;

CREATE TABLE urls (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) UNIQUE NOT NULL,
  created_at DATE NOT NULL
);

CREATE TABLE url_checks (
  id SERIAL PRIMARY KEY,
  url_id bigint REFERENCES urls(id),
  status_code SMALLINT,
  h1 VARCHAR(255),
  title VARCHAR(255),
  description VARCHAR(255),
  created_at DATE NOT NULL
);
