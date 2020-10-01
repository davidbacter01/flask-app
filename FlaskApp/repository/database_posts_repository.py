import psycopg2
from repository.posts_repository_interface import PostsRepositoryInterface
from models.blog_post import BlogPost
from setup.database import Database

class DatabasePostsRepository(PostsRepositoryInterface):
    ''' database management '''

    def __init__(self):
        self.database = Database()


    def add(self, post):
        '''adds a post to posts table in database'''

        conn = self.database.connect()
        cursor = conn.cursor()
        query = '''INSERT INTO posts (id, TITLE, OWNER, CONTENTS, CREATED_AT,
                MODIFIED_AT) VALUES (%s, %s, %s, %s, %s, %s)'''
        data = (
            post.blog_id,
            post.title,
            post.owner,
            post.contents,
            post.created_at,
            post.modified_at
            )
        cursor.execute(query, data)
        conn.commit()
        cursor.close()
        conn.close()


    def edit(self, post):
        ''' updates a post with same id as provided post '''

        old_post = self.get_by_id(post.blog_id)
        if post.title == old_post.title and post.contents == old_post.contents:
            return

        conn = self.database.connect()
        cursor = conn.cursor()
        cursor.execute('UPDATE posts SET MODIFIED_AT = %s WHERE ID = %s',
                       (post.modified_at, post.blog_id))
        if post.title != old_post.title:
            cursor.execute('UPDATE posts SET TITLE = %s WHERE ID = %s',
                           (post.title, post.blog_id))

        if post.contents != old_post.contents:
            cursor.execute('UPDATE posts SET CONTENTS = %s WHERE ID = %s',
                           (post.contents, post.blog_id))

        conn.commit()
        cursor.close()
        conn.close()


    def get_by_id(self, post_id):
        '''returns a post based on the id provided'''

        conn = self.database.connect()
        cursor = conn.cursor()
        query = '''SELECT * FROM posts WHERE ID = %s'''
        cursor.execute(query, (post_id,))
        data = cursor.fetchone()
        resulted_post = BlogPost(data[0], data[1], data[3], data[2])
        resulted_post.created_at = data[4]
        resulted_post.modified_at = data[5]
        conn.commit()
        cursor.close()
        conn.close()
        return resulted_post


    def get_all(self):
        conn = self.database.connect()
        cursor = conn.cursor()
        query = '''SELECT * FROM posts'''
        posts = []
        cursor.execute(query)
        entries = cursor.fetchall()
        for line in entries:
            resulted_post = BlogPost(line[0], line[1], line[3], line[2])
            resulted_post.created_at = line[4]
            resulted_post.modified_at = line[5]
            posts.insert(0, resulted_post)

        conn.commit()
        cursor.close()
        conn.close()
        return posts


    def remove(self, post_id):
        conn = self.database.connect()
        cursor = conn.cursor()
        query = '''DELETE FROM posts WHERE ID = %s'''
        cursor.execute(query, (post_id, ))
        conn.commit()
        cursor.close()
        conn.close()
