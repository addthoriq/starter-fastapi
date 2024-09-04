from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from ..config.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    posts = relationship('Post', back_populates='user')

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='posts')