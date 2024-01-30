CREATE KEYSPACE IF NOT EXISTS urlshortener
WITH replication = {
    'class': 'SimpleStrategy',
    'replication_factor': 2
};


CREATE TABLE IF NOT EXISTS urlshortener.urls (
    short_url text PRIMARY KEY,
    long_url text
);
