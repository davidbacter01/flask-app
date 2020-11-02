from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Date, ForeignKey

Base = declarative_base()


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    owner = Column(Integer, ForeignKey('users.id'))
    contents = Column(Integer, nullable=False)
    created_at = Column(Date)
    modified_at = Column(Date)
    user = relationship("User", back_populates="posts")

    def __repr__(self):
        return "<Post(title='{}', owner='{}')>" \
            .format(self.title, self.owner)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    created_at = Column(Date)
    modified_at = Column(Date)
    posts = relationship("Post", backref="users", cascade="all, delete")

    def __repr__(self):
        return "<Post(id='{}', name='{}', email={})>" \
            .format(self.id, self.name, self.email)
