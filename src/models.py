import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True, nullable=False)
    firstname = Column(String(50))
    lastname = Column(String(50))
    email = Column(String(120), unique=True)
    posts = relationship('Post')
    comments = relationship('Comment')
    followers = relationship('Follower', foreign_keys="[Follower.user_to_id]")
    following = relationship('Follower', foreign_keys="[Follower.user_from_id]")


class Follower(Base):
    __tablename__ = 'follower'
    user_from_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    user_to_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    follower = relationship('User', foreign_keys=[user_from_id])
    followed = relationship('User', foreign_keys=[user_to_id])


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User')
    comments = relationship('Comment')
    media = relationship('Media')


class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    type = Column(String(255), name="media_type_enum")
    url = Column(String(255), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'))
    post = relationship('Post')

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    comment_text = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    author = relationship('User')
    post = relationship('Post')


try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e