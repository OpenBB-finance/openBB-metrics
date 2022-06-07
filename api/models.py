from typing import Any
from sqlalchemy import (Column, Integer, String)
from . import database

Base: Any = database.Base


class TerminalDownloads(Base):
    __tablename__ = "terminal_download"

    id = Column(Integer, primary_key=True, index=True)
    tag_name = Column(String, nullable=True)
    macos = Column(Integer, nullable=True)
    windows = Column(Integer, nullable=True)
    updated_date = Column(String, nullable=False)


class Twitter(Base):
    __tablename__ = "twitter"

    id = Column(Integer, primary_key=True, index=True)
    total_followers = Column(Integer, nullable=True)
    new_followers = Column(Integer, nullable=True)
    likes = Column(Integer, nullable=True)
    retweets = Column(Integer, nullable=True)
    updated_date = Column(String, nullable=False)


class Reddit(Base):
    __tablename__ = "reddit"

    id = Column(Integer, primary_key=True, index=True)
    total_followers = Column(Integer, nullable=True)
    new_followers = Column(Integer, nullable=True)
    upvotes = Column(Integer, nullable=True)
    updated_date = Column(String, nullable=False)
