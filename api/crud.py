from typing import Union
from sqlalchemy.orm import Session
from . import models, schemas


def get_terminal_downloads(db: Session, updated_date: Union[str, None] = None):
    if updated_date:
        return db.query(models.TerminalDownloads).filter(models.TerminalDownloads.updated_date == updated_date).first()
    else:
        return db.query(models.TerminalDownloads).all()


def create_terminal_download(db: Session, terminal: schemas.TerminalCreate):
    db_download = models.TerminalDownloads(tag_name=terminal.tag_name, macos=terminal.macos,
                                           windows=terminal.windows, updated_date=terminal.updated_date)
    db.add(db_download)
    db.commit()
    db.refresh(db_download)
    return db_download


def get_twitter(db: Session, updated_date: Union[str, None] = None):
    if updated_date:
        return db.query(models.Twitter).filter(models.Twitter.updated_date == updated_date).first()
    else:
        return db.query(models.Twitter).all()


def create_twitter(db: Session, twitter: schemas.TwitterCreate):
    db_twitter = models.Twitter(total_followers=twitter.total_followers, new_followers=twitter.new_followers,
                                likes=twitter.likes, retweets=twitter.retweets, mentions=twitter.mentions,
                                updated_date=twitter.updated_date)
    db.add(db_twitter)
    db.commit()
    db.refresh(db_twitter)
    return db_twitter


def get_reddit(db: Session, updated_date: Union[str, None] = None):
    if updated_date:
        return db.query(models.Reddit).filter(models.Reddit.updated_date == updated_date).first()
    else:
        return db.query(models.Reddit).all()


def create_reddit(db: Session, reddit: schemas.RedditCreate):
    db_reddit = models.Reddit(total_followers=reddit.total_followers, new_followers=reddit.new_followers,
                              upvotes=reddit.upvotes, updated_date=reddit.updated_date)
    db.add(db_reddit)
    db.commit()
    db.refresh(db_reddit)
    return db_reddit


def get_linkedin(db: Session):
    return db.query(models.Linkedin).all()


def create_linkedin(db: Session, linkedin: schemas.LinkedinCreate):
    db_linkedin = models.Linkedin(total_followers=linkedin.total_followers, new_followers=linkedin.new_followers,
                                  updated_date=linkedin.updated_date)
    db.add(db_linkedin)
    db.commit()
    db.refresh(db_linkedin)
    return db_linkedin


def get_discord(db: Session):
    return db.query(models.Discord).all()


def create_discord(db: Session, discord: schemas.LinkedinCreate):
    db_discord = models.Discord(total_followers=discord.total_followers, new_followers=discord.new_followers,
                                active_followers=discord.active_followers, updated_date=discord.updated_date)
    db.add(db_discord)
    db.commit()
    db.refresh(db_discord)
    return db_discord


def get_headlines(db: Session, url: Union[str, None] = None):
    if url:
        return db.query(models.Headlines).filter(models.Headlines.url == url).first()
    else:
        return db.query(models.Headlines).all()


def create_headlines(db: Session, headlines: schemas.HeadlinesCreate):
    db_headlines = models.Headlines(source=headlines.source, title=headlines.title, url=headlines.url,
                                    published_date=headlines.published_date)
    db.add(db_headlines)
    db.commit()
    db.refresh(db_headlines)
    return db_headlines


def get_youtube(db: Session, video_id: Union[str, None] = None):
    if video_id:
        return db.query(models.Youtube).filter(models.Youtube.video_id == video_id).first()
    else:
        return db.query(models.Youtube).all()


def create_youtube(db: Session, youtube: schemas.YoutubeCreate):
    db_youtube = models.Youtube(channel=youtube.channel, title=youtube.title, video_id=youtube.video_id,
                                published_date=youtube.published_date)
    db.add(db_youtube)
    db.commit()
    db.refresh(db_youtube)
    return db_youtube
