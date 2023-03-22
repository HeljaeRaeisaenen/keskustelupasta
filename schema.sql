CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, passwordhash TEXT);

CREATE TABLE posts (id SERIAL PRIMARY KEY, title TEXT, message TEXT, time TIMESTAMP, user_id INTEGER REFERENCES users, topic_id INTEGER REFERENCES topics);

CREATE TABLE comments (id SERIAL PRIMARY KEY, message TEXT, time TIMESTAMP, user_id INTEGER REFERENCES users, post_id INTEGER REFERENCES posts);

CREATE TABLE topics (id SERIAL PRIMARY KEY, topic TEXT);

CREATE TABLE admins (id SERIAL PRIMARY KEY, username TEXT, passwordhash TEXT);


