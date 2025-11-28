# main.py (snippet)
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base

app = FastAPI()

# create tables (only needed once at startup)
Base.metadata.create_all(bind=engine)

# dependency for routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root(db: Session = Depends(get_db)):
    # you can use db here to query
    return {"message": "DB ready"}
