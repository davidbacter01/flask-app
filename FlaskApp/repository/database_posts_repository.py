from datetime import datetime
import os
from sqlalchemy import desc
from repository.posts_repository_interface import PostsRepositoryInterface
from models.blog_post import BlogPost
from database.post import Post
from database.user import User


class DatabasePostsRepository(PostsRepositoryInterface):
    """ database management """

    def __init__(self, database, session):
        self.database = database
        self.session = session

    def count(self, user=None):
        """counts posts owned by user (if None, counts all)"""
        session = self.session()
        count = 0
        if user not in (None, 'All', ''):
            usr = session.query(User).filter_by(name=user).first()
            count = session.query(Post).filter(Post.owner == usr.id).count()
        else:
            count = session.query(Post).count()
        session.commit()
        session.close()
        return count

    def add(self, post):
        """adds a post to posts table in database"""
        session = self.session()
        image = post.image
        if not isinstance(post.image, str):
            image = post.image.filename
        new_post = Post(title=post.title,
                        owner=post.owner,
                        contents=post.contents,
                        image=image,
                        created_at=post.created_at,
                        modified_at=datetime.now()
                        )
        session.add(new_post)
        session.commit()
        if not isinstance(post.image, str):
            post.image.filename = str(new_post.id) + '.png'
            new_post.image = post.image.filename
            session.commit()
            post.image.save(os.path.join('./static/img', post.image.filename))
        session.close()

    def edit(self, post: BlogPost):
        """ updates a post with same id as provided post """
        session = self.session()
        to_edit = session.query(Post).filter_by(id=post.blog_id).first()
        to_edit.title = post.title
        to_edit.contents = post.contents
        if post.image:
            if to_edit.image == 'default_blog.png':
                post.image.filename = str(to_edit.id) + '.png'
            else:
                post.image.filename = '0'+ str(to_edit.image)
            if os.path.exists("./static/img/" + str(to_edit.image))\
            and str(to_edit.image) != 'default_blog.png':
                os.remove("./static/img/" + str(to_edit.image))
            to_edit.image = post.image.filename
            post.image.save(os.path.join('./static/img', post.image.filename))
        to_edit.modified_at = post.modified_at
        session.commit()
        session.close()

    def get_by_id(self, post_id):
        """returns a post based on the id provided"""
        session = self.session()
        post = session.query(Post).filter_by(id=post_id).first()
        session.commit()
        result = BlogPost(
            post.title,
            post.contents,
            post.user.name
            )
        result.blog_id = post.id
        result.image = post.image
        result.created_at = post.created_at
        result.modified_at = post.modified_at
        session.close()
        return result

    def get_all(self, owner, page_current):
        offset = (int(page_current) - 1) * 5
        session = self.session()
        result = None
        if owner in ('All', None):
            result = session.query(Post).order_by(desc(Post.id)).limit(5).offset(offset).all()
        else:
            result = session.query(User).filter_by(name=owner).first().posts[offset:offset+5]
        session.commit()
        posts = []
        for post in result:
            res = BlogPost(
                post.title,
                post.contents,
                post.user.name
                )
            res.blog_id = post.id
            res.image = post.image
            res.created_at = post.created_at
            res.modified_at = post.modified_at
            posts.append(res)
        session.close()
        return posts

    def remove(self, post_id):
        session = self.session()
        post = session.query(Post).filter_by(id=post_id).first()
        session.commit()
        if os.path.exists("./static/img/" + str(post.image))\
            and str(post.image) != 'default_blog.png':
            os.remove("./static/img/" + str(post.image))
        session.delete(post)
        session.commit()
        session.close()
