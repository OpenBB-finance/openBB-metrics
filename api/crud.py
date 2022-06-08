from sqlalchemy.orm import Session
from . import models, schemas


def get_terminal_downloads(db: Session):
    return db.query(models.TerminalDownloads).all()


def create_terminal_download(db: Session, terminal: schemas.TerminalCreate):
    db_download = models.TerminalDownloads(tag_name=terminal.tag_name, macos=terminal.macos,
                                           windows=terminal.windows, updated_date=terminal.updated_date)
    db.add(db_download)
    db.commit()
    db.refresh(db_download)
    return db_download


def get_twitter(db: Session):
    return db.query(models.Twitter).all()


def create_twitter(db: Session, twitter: schemas.TwitterCreate):
    db_twitter = models.Twitter(total_followers=twitter.total_followers, new_followers=twitter.new_followers,
                                likes=twitter.likes, retweets=twitter.retweets, updated_date=twitter.updated_date)
    db.add(db_twitter)
    db.commit()
    db.refresh(db_twitter)
    return db_twitter


def get_reddit(db: Session):
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
