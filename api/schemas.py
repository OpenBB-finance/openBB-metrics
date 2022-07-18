from typing import Any, Optional
from pydantic import BaseModel, Extra

main_config = {"orm_mode": True, "extra": Extra.forbid}


class TerminalCreate(BaseModel, **main_config):
    tag_name: Optional[str]
    macos: Optional[int]
    windows: Optional[int]
    updated_date: int


class TerminalReturn(BaseModel, **main_config):
    tag_name: str
    macos: Optional[int]
    windows: Optional[int]
    updated_date: int


class TwitterCreate(BaseModel, **main_config):
    total_followers: Optional[int]
    new_followers: Optional[int]
    likes: Optional[int]
    retweets: Optional[int]
    mentions: Optional[int]
    updated_date: int


class TwitterReturn(BaseModel, **main_config):
    total_followers: Optional[int]
    new_followers: Optional[int]
    likes: Optional[int]
    retweets: Optional[int]
    mentions: Optional[int]
    updated_date: int


class RedditCreate(BaseModel, **main_config):
    total_followers: Optional[int]
    new_followers: Optional[int]
    upvotes: Optional[int]
    updated_date: int


class RedditReturn(BaseModel, **main_config):
    total_followers: Optional[int]
    new_followers: Optional[int]
    upvotes: Optional[int]
    updated_date: int


class LinkedinCreate(BaseModel, **main_config):
    total_followers: Optional[int]
    new_followers: Optional[int]
    updated_date: int


class LinkedinReturn(BaseModel, **main_config):
    total_followers: Optional[int]
    new_followers: Optional[int]
    updated_date: int


class DiscordCreate(BaseModel, **main_config):
    total_followers: Optional[int]
    new_followers: Optional[int]
    active_followers: Optional[int]
    updated_date: int


class DiscordReturn(BaseModel, **main_config):
    total_followers: Optional[int]
    new_followers: Optional[int]
    active_followers: Optional[int]
    updated_date: int


class HeadlinesCreate(BaseModel, **main_config):
    source: Optional[str]
    title: Optional[str]
    url: Optional[str]
    published_date: int


class HeadlinesReturn(BaseModel, **main_config):
    source: Optional[str]
    title: Optional[str]
    url: Optional[str]
    published_date: int


class YoutubeCreate(BaseModel, **main_config):
    channel: Optional[str]
    title: Optional[str]
    video_id: Optional[str]
    published_date: int


class YoutubeReturn(BaseModel, **main_config):
    channel: Optional[str]
    title: Optional[str]
    video_id: Optional[str]
    published_date: int


class GithubCreate(BaseModel, **main_config):
    contributors: Optional[int]
    stars: Optional[int]
    forks: Optional[int]
    open_pr: Optional[int]
    closed_pr: Optional[int]
    issues: Optional[int]
    updated_date: int


class GithubReturn(BaseModel, **main_config):
    contributors: Optional[int]
    stars: Optional[int]
    forks: Optional[int]
    open_pr: Optional[int]
    closed_pr: Optional[int]
    issues: Optional[int]
    updated_date: int


class MessageReturn(BaseModel, **main_config):
    message: str
    success: bool
    features: Optional[Any]
