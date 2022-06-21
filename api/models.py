from typing import Any
from sqlalchemy import (Column, Integer, String, UniqueConstraint)
from . import database

Base: Any = database.Base


class TerminalDownloads(Base):
    __tablename__ = "terminal_download"
    __table_args__ = (UniqueConstraint('updated_date'),)

    id = Column(Integer, primary_key=True, index=True)
    tag_name = Column(String, nullable=True)
    macos = Column(Integer, nullable=True)
    windows = Column(Integer, nullable=True)
    updated_date = Column(String, nullable=False)


class Twitter(Base):
    __tablename__ = "twitter"
    __table_args__ = (UniqueConstraint('updated_date'),)

    id = Column(Integer, primary_key=True, index=True)
    total_followers = Column(Integer, nullable=True)
    new_followers = Column(Integer, nullable=True)
    likes = Column(Integer, nullable=True)
    retweets = Column(Integer, nullable=True)
    mentions = Column(Integer, nullable=True)
    updated_date = Column(String, nullable=False)


class Reddit(Base):
    __tablename__ = "reddit"
    __table_args__ = (UniqueConstraint('updated_date'),)

    id = Column(Integer, primary_key=True, index=True)
    total_followers = Column(Integer, nullable=True)
    new_followers = Column(Integer, nullable=True)
    upvotes = Column(Integer, nullable=True)
    updated_date = Column(String, nullable=False)


class Linkedin(Base):
    __tablename__ = "linkedin"

    id = Column(Integer, primary_key=True, index=True)
    total_followers = Column(Integer, nullable=True)
    new_followers = Column(Integer, nullable=True)
    updated_date = Column(String, nullable=False)


class Discord(Base):
    __tablename__ = "discord"

    id = Column(Integer, primary_key=True, index=True)
    total_followers = Column(Integer, nullable=True)
    new_followers = Column(Integer, nullable=True)
    active_followers = Column(Integer, nullable=True)
    updated_date = Column(String, nullable=False)


class Headlines(Base):
    __tablename__ = "headlines"
    __table_args__ = (UniqueConstraint('url', 'published_date'),)

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String)
    title = Column(String)
    url = Column(String)
    published_date = Column(String)


class Youtube(Base):
    __tablename__ = "youtube"
    __table_args__ = (UniqueConstraint('video_id'),)

    id = Column(Integer, primary_key=True, index=True)
    channel = Column(String)
    title = Column(String)
    video_id = Column(String, unique=True)
    published_date = Column(String)
