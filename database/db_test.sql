DROP DATABASE IF EXISTS test_predicta_app;
CREATE DATABASE test_predicta_app;

\c test_predicta_app

DROP TABLE IF EXISTS user_info;
CREATE TABLE user_info (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR,
    last_name VARCHAR
);

DROP TABLE IF EXISTS user_prediction;
CREATE TABLE user_prediction (
    prediction_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES user_info(user_id),
    prediction VARCHAR,
    friend_name VARCHAR,
    friend_prediction VARCHAR,
    stake INT NULL,
    created_at TIMESTAMP 
);