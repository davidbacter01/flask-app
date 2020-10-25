CREATE_TABLE_POSTS = '''CREATE TABLE IF NOT EXISTS posts
                (id SERIAL PRIMARY KEY UNIQUE NOT NULL,
                title TEXT NOT NULL,
                owner TEXT NOT NULL,
                contents TEXT NOT NULL,
                created_at TIMESTAMP,
                modified_at TIMESTAMP)'''

CREATE_TABLE_USERS = '''CREATE TABLE IF NOT EXISTS users
(
    id SERIAL PRIMARY KEY UNIQUE NOT NULL,
    name text UNIQUE NOT NULL,
    email text,
    password VARCHAR(100),
    created_at timestamp without time zone,
    modified_at timestamp without time zone
)'''

ADD_OWNERS_AS_USERS = '''INSERT INTO users(name)
SELECT DISTINCT owner FROM posts
WHERE CAST(posts.owner AS TEXT) NOT IN (SELECT CAST(id AS TEXT) FROM users)
ON CONFLICT DO NOTHING
'''

UPDATE_DATE_OF_CREATION = '''UPDATE users
SET created_at=now()::timestamp(0), modified_at=now()::timestamp(0)
WHERE users.created_at is null and users.name is not null
'''

ADD_ADMIN = '''
INSERT INTO users (name, email, password, created_at, modified_at)
VALUES ('admin', 'admin', 'admin', now()::timestamp(0), now()::timestamp(0))
ON CONFLICT DO NOTHING'''

INSERT_WHITESPACE_FOR_NOT_NULL = '''UPDATE users SET
email='1',
password='1'
WHERE created_at is null
'''

SET_NOT_NULL_FIELDS_IN_USERS = '''
ALTER TABLE users
ALTER COLUMN email SET NOT NULL,
ALTER COLUMN password SET NOT NULL
'''

UPDATE_POST_OWNER = '''UPDATE posts
SET owner=users.id
FROM users 
WHERE CAST(posts.owner AS TEXT)=users.name OR CAST(posts.owner AS TEXT)=CAST(users.id AS TEXT)
'''

ALTER_OWNER_TO_INT = '''ALTER TABLE posts ALTER COLUMN owner TYPE INTEGER USING owner::integer'''


CREATE_FUNCTION_TO_DROP_ALL_FOREIGN_KEYS = '''
create or replace function remove_fk_by_table_and_column(p_table_name 
varchar, p_column_name varchar) returns INTEGER as $$
declare
     v_fk_name varchar := NULL;
     v_fk_num_removed INTEGER := 0;
begin
     FOR v_fk_name IN (SELECT ss2.conname
         FROM pg_attribute af, pg_attribute a,
             (SELECT conname, conrelid,confrelid,conkey[i] AS conkey, 
confkey[i] AS confkey
                 FROM (SELECT conname, conrelid,confrelid,conkey,confkey,
                     generate_series(1,array_upper(conkey,1)) AS i
                     FROM pg_constraint WHERE contype = 'f') ss) ss2
         WHERE af.attnum = confkey
             AND af.attrelid = confrelid
             AND a.attnum = conkey
             AND a.attrelid = conrelid
             AND a.attrelid = p_table_name::regclass
             AND a.attname = p_column_name) LOOP
         execute 'alter table ' || quote_ident(p_table_name) || ' drop 
constraint ' || quote_ident(v_fk_name);
         v_fk_num_removed = v_fk_num_removed + 1;
     END LOOP;
     return v_fk_num_removed;
end;
$$ language plpgsql;
'''


DROP_ALL_FOREIGN_KEYS_ON_POST_OWNER = '''
select remove_fk_by_table_and_column('posts', 'owner')
'''


ADD_FOREIGN_KEY = '''ALTER TABLE posts
ADD FOREIGN KEY (owner) REFERENCES users (id)
ON DELETE CASCADE
'''

updates = [
    CREATE_TABLE_POSTS,
    CREATE_TABLE_USERS,
    ADD_OWNERS_AS_USERS,
    UPDATE_DATE_OF_CREATION,
    ADD_ADMIN,
    INSERT_WHITESPACE_FOR_NOT_NULL,
    SET_NOT_NULL_FIELDS_IN_USERS,
    UPDATE_POST_OWNER,
    ALTER_OWNER_TO_INT,
    CREATE_FUNCTION_TO_DROP_ALL_FOREIGN_KEYS,
    DROP_ALL_FOREIGN_KEYS_ON_POST_OWNER,
    ADD_FOREIGN_KEY
    ]
