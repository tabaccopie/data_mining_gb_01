import datetime as dt
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Table,
    DateTime,
    Boolean
)

Base = declarative_base()
tag_post = Table(
    "tag_post",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("post.id")),
    Column("tag_id", Integer, ForeignKey("tag.id")),
)


class IdM:
    id = Column(Integer, primary_key=True, autoincrement=True)


class NameM:
    name = Column(String, nullable=False)


class UrlM:
    url = Column(String, nullable=False, unique=True)


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    url = Column(String(2048), nullable=False, unique=True)
    title = Column(String, nullable=False, unique=False)
    author_id = Column(Integer, ForeignKey("author.id"), nullable=False)
    author = relationship("Author", backref="posts")
    tags = relationship("Tag", secondary=tag_post)
    comments = relationship("Comment")


class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(2048), nullable=False, unique=True)
    name = Column(String(250), nullable=False, unique=False)


class Tag(Base, IdM, NameM, UrlM):
    __tablename__ = "tag"
    posts = relationship("Post", secondary=tag_post)


class Comment(Base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("comment.id"), nullable=True)
    likes_count = Column(Integer)
    body = Column(String)
    created_at = Column(DateTime, nullable=False)
    hidden = Column(Boolean)
    deep = Column(Integer)
    author_id = Column(Integer, ForeignKey("author.id"))
    author = relationship("Author")
    time_now = Column(DateTime)
    post_id = Column(Integer, ForeignKey("post.id"))

    def __init__(self, **kwargs):
        self.id = kwargs["id"]
        self.parent_id = kwargs["parent_id"]
        self.likes_count = kwargs["likes_count"]
        self.body = kwargs["body"]
        self.created_at = dt.datetime.fromisoformat(kwargs["created_at"])
        self.hidden = kwargs["hidden"]
        self.deep = kwargs["deep"]
        self.time_now = dt.datetime.fromisoformat(kwargs["time_now"])
        self.author = kwargs["author"]
