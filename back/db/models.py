from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Boolean, DateTime,  Integer, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


Base = declarative_base()


class ModelBase(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Users(ModelBase):
    __tablename__ = "users"

    email = Column(String, unique=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)

    comments = relationship("Comments", back_populates="user")
    posts = relationship("Posts", back_populates="user")


class Posts(ModelBase):
    __tablename__ = "posts"

    text = Column(String)
    likes = Column(Integer, default=0)

    comments = relationship("Comments", back_populates="post")
    user = relationship(Users, back_populates="posts")

    user_id = Column(Integer, ForeignKey("users.id"))


class Comments(ModelBase):
    __tablename__ = "comments"

    text = Column(String)
    likes = Column(Integer, default=0)
    
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    
    post = relationship(Posts, back_populates="comments")
    user = relationship(Users, back_populates="comments")
    
