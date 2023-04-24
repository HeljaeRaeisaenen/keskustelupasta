DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS topics CASCADE;
DROP TABLE IF EXISTS posts CASCADE;
DROP TABLE IF EXISTS comments CASCADE;

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
INSERT INTO users (username, passwordhash, admin) VALUES ('admin', 'pbkdf2:sha256:260000$mqCnyWZLhohi6ouK$f0c2a8c06571ee0dc28a80074ce04b9943e38d0d403dbd9ba3dabcaa99da6820', '1');
INSERT INTO topics (topic) VALUES ('Spaghetti Bolognaise');
INSERT INTO topics (topic) VALUES ('Lasagne');
INSERT INTO topics (topic) VALUES ('Fettuccine Alfredo');

