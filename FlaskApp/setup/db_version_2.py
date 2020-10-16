CREATE_TABLE_USERS = '''CREATE TABLE IF NOT EXISTS users
(
    id SERIAL PRIMARY KEY UNIQUE NOT NULL,
    name text UNIQUE NOT NULL,
    email text UNIQUE,
    password VARCHAR(30),
    created_at timestamp without time zone,
    modified_at timestamp without time zone
)'''

ADD_OWNERS_AS_USERS = '''INSERT INTO users(name)
SELECT DISTINCT owner FROM posts
WHERE CAST(posts.owner AS TEXT) NOT IN (SELECT CAST(id AS TEXT) FROM users)
'''

INSERT_WHITESPACE_FOR_NOT_NULL = '''UPDATE users SET
email='',
password=''
'''

SET_NOT_NULL_FIELDS_IN_USERS = '''
ALTER TABLE users
ALTER COLUMN email SET NOT NULL,
ALTER COLUMN password SET NOT NULL;
'''

UPDATE_POST_OWNER = '''UPDATE posts
SET owner=users.id
FROM users 
WHERE CAST(posts.owner AS TEXT)=users.name
'''

ALTER_OWNER_TO_INT = '''ALTER TABLE posts ALTER COLUMN owner TYPE INTEGER USING owner::integer'''

ADD_FOREIGN_KEY = '''ALTER TABLE posts
ADD FOREIGN KEY (owner) REFERENCES users (id)
'''

updates = [
    CREATE_TABLE_USERS,
    ADD_OWNERS_AS_USERS,
    INSERT_WHITESPACE_FOR_NOT_NULL,
    SET_NOT_NULL_FIELDS_IN_USERS,
    UPDATE_POST_OWNER,
    ALTER_OWNER_TO_INT,
    ADD_FOREIGN_KEY
    ]
