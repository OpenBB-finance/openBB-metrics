from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, StarletteHTTPException
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from api import crud, models, schemas
from api.database import *

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

SUCCESS = JSONResponse(content={"success": "true"}, status_code=200)
DUPLICATE = JSONResponse(content={"success": "false - duplicate entry"}, status_code=409)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


@app.get("/")
def home():
    return {"/terminal_downloads": "Terminal Download Statistics",
            "/twitter": "Twitter Statistics",
            "/reddit": "Reddit Statistics",
            "/headlines": "News Headlines Statistics",
            "/youtube": "Youtube Statistics"}


@app.get("/terminal_downloads")
def get_terminal_downloads(db: Session = Depends(get_db)):
    return crud.get_terminal_downloads(db)


@app.post("/terminal_downloads", response_model=schemas.MessageReturn)
def create_terminal_downloads(terminal: schemas.TerminalCreate, db: Session = Depends(get_db)):
    db_terminal = crud.get_terminal_downloads(db, terminal.updated_date)
    if db_terminal:
        return DUPLICATE
    crud.create_terminal_download(db=db, terminal=terminal)
    return SUCCESS


@app.get("/twitter")
def get_twitter(db: Session = Depends(get_db)):
    return crud.get_twitter(db)


@app.post("/twitter", response_model=schemas.MessageReturn)
def create_twitter(twitter: schemas.TwitterCreate, db: Session = Depends(get_db)):
    db_twitter = crud.get_twitter(db, twitter.updated_date)
    if db_twitter:
        return DUPLICATE
    crud.create_twitter(db=db, twitter=twitter)
    return SUCCESS


@app.get("/reddit")
def get_reddit(db: Session = Depends(get_db)):
    return crud.get_reddit(db)


@app.post("/reddit", response_model=schemas.MessageReturn)
def create_reddit(reddit: schemas.RedditCreate, db: Session = Depends(get_db)):
    db_reddit = crud.get_reddit(db, reddit.updated_date)
    if db_reddit:
        return DUPLICATE
    crud.create_reddit(db=db, reddit=reddit)
    return SUCCESS


@app.get("/linkedin")
def get_linkedin(db: Session = Depends(get_db)):
    return crud.get_linkedin(db)


@app.get("/discord")
def get_discord(db: Session = Depends(get_db)):
    return crud.get_discord(db)


@app.get("/headlines")
def get_headlines(db: Session = Depends(get_db)):
    return crud.get_headlines(db)


@app.post("/headlines", response_model=schemas.MessageReturn)
def create_headlines(headlines: schemas.HeadlinesCreate, db: Session = Depends(get_db)):
    db_headlines = crud.get_headlines(db, headlines.url)
    if db_headlines:
        return DUPLICATE
    crud.create_headlines(db=db, headlines=headlines)
    return SUCCESS


@app.get("/youtube")
def get_youtube(db: Session = Depends(get_db)):
    return crud.get_youtube(db)


@app.post("/youtube", response_model=schemas.MessageReturn)
def create_youtube(youtube: schemas.YoutubeCreate, db: Session = Depends(get_db)):
    db_youtube = crud.get_youtube(db, youtube.video_id)
    if db_youtube:
        return DUPLICATE
    crud.create_youtube(db=db, youtube=youtube)
    return SUCCESS
