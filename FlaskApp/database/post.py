from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Date, ForeignKey

Base = declarative_base()


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    owner = Column(Integer, ForeignKey('users.id'))
    contents = Column(String, nullable=False)
    image = Column(String, nullable=False, default='default_blog.png')
    created_at = Column(Date)
    modified_at = Column(Date)
    user = relationship("User", back_populates="posts")

    def __repr__(self):
        return "<Post(title='{}', owner='{}')>" \
            .format(self.title, self.owner)
