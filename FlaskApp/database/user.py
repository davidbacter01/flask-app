from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Date
from database.post import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(Date)
    modified_at = Column(Date)
    posts = relationship("Post", backref="users", cascade="all, delete")

    def __repr__(self):
        return "<Post(id='{}', name='{}', email={})>" \
            .format(self.id, self.name, self.email)
