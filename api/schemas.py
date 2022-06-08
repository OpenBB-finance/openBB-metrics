from typing import Any, Optional
from pydantic import BaseModel, Extra

main_config = {"orm_mode": True, "extra": Extra.forbid}


class TerminalCreate(BaseModel, **main_config):
    tag_name: Optional[str]
    macos: Optional[int]
    windows: Optional[int]
    updated_date: str


class TerminalReturn(BaseModel, **main_config):
    tag_name: str
    macos: Optional[int]
    windows: Optional[int]
    updated_date: str


class TwitterCreate(BaseModel, **main_config):
    total_followers: Optional[int]
    new_followers: Optional[int]
    likes: Optional[int]
    retweets: Optional[int]
    updated_date: str


class TwitterReturn(BaseModel, **main_config):
    total_followers: Optional[int]
    new_followers: Optional[int]
    likes: Optional[int]
    retweets: Optional[int]
    updated_date: str


class RedditCreate(BaseModel, **main_config):
    total_followers: Optional[int]
    new_followers: Optional[int]
    upvotes: Optional[int]
    updated_date: str


class RedditReturn(BaseModel, **main_config):
    total_followers: Optional[int]
    new_followers: Optional[int]
    upvotes: Optional[int]
    updated_date: str


class LinkedinCreate(BaseModel, **main_config):
    total_followers: Optional[int]
    new_followers: Optional[int]
    updated_date: str


class LinkedinReturn(BaseModel, **main_config):
    total_followers: Optional[int]
    new_followers: Optional[int]
    updated_date: str


class DiscordCreate(BaseModel, **main_config):
    total_followers: Optional[int]
    new_followers: Optional[int]
    active_followers: Optional[int]
    updated_date: str


class DiscordReturn(BaseModel, **main_config):
    total_followers: Optional[int]
    new_followers: Optional[int]
    active_followers: Optional[int]
    updated_date: str


class MessageReturn(BaseModel, **main_config):
    message: str
    success: bool
    features: Optional[Any]
