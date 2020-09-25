import psycopg2
from repository.posts_repository_interface import PostsRepositoryInterface
from models.blog_post import BlogPost

#conn = psycopg2.connect("dbname=suppliers user=postgres password=postgres")

class DatabasePostsRepository(PostsRepositoryInterface):
    ''' database management '''

    def __init__(self, credentials):
        self.credentials = credentials


    def __extract_post_from_query_result__(self, post_data):
        ''' parses a table line to a BlogPost object '''

        resulted_post = BlogPost(post_data[0], post_data[1], post_data[3], post_data[2])
        resulted_post.created_at = post_data[4]
        resulted_post.modified_at = post_data[5]
        return resulted_post


    def add(self, post):
        '''adds a post to posts table in database'''

        conn = psycopg2.connect(self.credentials)
        cursor = conn.cursor()
        SQL = '''INSERT INTO posts (id, TITLE, OWNER, CONTENTS, CREATED_AT,
                MODIFIED_AT) VALUES (%s, %s, %s, %s, %s, %s)'''
        data = (
            post.id,
            post.title,
            post.owner,
            post.contents,
            post.created_at,
            post.modified_at
            )
        cursor.execute(SQL, data)
        conn.commit()
        cursor.close()
        conn.close()


    def edit(self, post):
        ''' updates a post with same id as provided post '''

        old_post = self.get_by_id(post.id)
        if post.title == old_post.title and post.contents == old_post.contents: return

        conn = psycopg2.connect(self.credentials)
        cursor = conn.cursor()
        cursor.execute('UPDATE posts SET MODIFIED_AT = %s WHERE ID = %s',
                       (post.modified_at, post.id))
        if post.title != old_post.title:
            cursor.execute('UPDATE posts SET TITLE = %s WHERE ID = %s',
                           (post.title, post.id))

        if post.contents != old_post.contents:
            cursor.execute('UPDATE posts SET CONTENTS = %s WHERE ID = %s',
                           (post.contents, post.id))

        conn.commit()
        cursor.close()
        conn.close()


    def get_by_id(self, post_id):
        '''returns a post based on the id provided'''

        conn = psycopg2.connect(self.credentials)
        cursor = conn.cursor()
        query = '''SELECT * FROM posts WHERE ID = %s'''
        cursor.execute(query, (post_id,))
        data = cursor.fetchone()
        resulted_post = self.__extract_post_from_query_result__(data)        
        conn.commit()
        cursor.close()
        conn.close()
        return resulted_post


    def get_all(self):
        conn = psycopg2.connect(self.credentials)
        cursor = conn.cursor()
        query = '''SELECT * FROM posts'''
        posts = []
        cursor.execute(query)
        entries = cursor.fetchall()
        for line in entries:
            posts.insert(0, self.__extract_post_from_query_result__(line))

        conn.commit()
        cursor.close()
        conn.close()
        return posts


    def remove(self, post_id):
        conn = psycopg2.connect(self.credentials)
        cursor = conn.cursor()
        query = '''DELETE FROM posts WHERE ID = %s'''
        cursor.execute(query, (post_id, ))
        conn.commit()
        cursor.close()
        conn.close()
