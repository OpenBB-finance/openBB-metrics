from sqlalchemy.orm import Session
from . import models, schemas


def get_terminal_download(db: Session, updated_date: int):
    return db.query(models.TerminalDownloads).filter(models.TerminalDownloads.updated_date == updated_date).first()


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
