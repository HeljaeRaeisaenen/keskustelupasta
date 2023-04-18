CREATE TABLE users (
	id SERIAL PRIMARY KEY, 
	username TEXT UNIQUE, 
	passwordhash TEXT, 
	admin BOOLEAN);

CREATE TABLE topics (
        id SERIAL PRIMARY KEY,
        topic TEXT UNIQUE);

CREATE TABLE posts (
	id SERIAL PRIMARY KEY, 
	title TEXT, message TEXT, 
	time TIMESTAMP, 
	user_id INTEGER REFERENCES users ON DELETE CASCADE, 
	topic_id INTEGER REFERENCES topics ON DELETE CASCADE);

CREATE TABLE comments (
	id SERIAL PRIMARY KEY, 
	message TEXT, 
	time TIMESTAMP, 
	user_id INTEGER REFERENCES users ON DELETE CASCADE, 
	post_id INTEGER REFERENCES posts ON DELETE CASCADE);

INSERT INTO users (username, passwordhash, admin) VALUES ('deleted user','','0');
