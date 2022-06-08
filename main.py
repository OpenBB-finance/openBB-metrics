from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, StarletteHTTPException
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from api import crud, models, schemas
from api.database import *

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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
            "/reddit": "Reddit Statistics"}


@app.get("/terminal_downloads")
def get_terminal_downloads(db: Session = Depends(get_db)):
    return crud.get_terminal_downloads(db)


@app.post("/terminal_downloads", response_model=schemas.MessageReturn)
def create_terminal_downloads(terminal: schemas.TerminalCreate, db: Session = Depends(get_db)):
    crud.create_terminal_download(db=db, terminal=terminal)
    return JSONResponse(content={"success": "true"}, status_code=200)


@app.get("/twitter")
def get_twitter(db: Session = Depends(get_db)):
    return crud.get_twitter(db)


@app.post("/twitter", response_model=schemas.MessageReturn)
def create_twitter(twitter: schemas.TwitterCreate, db: Session = Depends(get_db)):
    crud.create_twitter(db=db, twitter=twitter)
    return JSONResponse(content={"success": "true"}, status_code=200)


@app.get("/reddit")
def get_reddit(db: Session = Depends(get_db)):
    return crud.get_reddit(db)


@app.post("/reddit", response_model=schemas.MessageReturn)
def create_reddit(reddit: schemas.RedditCreate, db: Session = Depends(get_db)):
    crud.create_reddit(db=db, reddit=reddit)
    return JSONResponse(content={"success": "true"}, status_code=200)


@app.get("/linkedin")
def get_linkedin(db: Session = Depends(get_db)):
    return crud.get_linkedin(db)


@app.get("/discord")
def get_discord(db: Session = Depends(get_db)):
    return crud.get_discord(db)
