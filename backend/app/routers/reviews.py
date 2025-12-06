from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.schemas import *
from app.crud.reviews import create_review, list_reviews, get_stats
from app.db import session_maker

router = APIRouter(prefix="/reviews", tags=["reviews"])

def get_db():
    db = session_maker()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ReviewOut)
def create_review_endpoint(payload: ReviewCreate, db: Session = Depends(get_db)):
    obj = create_review(db, payload)
    return obj

@router.get("/", response_model=list[ReviewOut])
def list_reviews_endpoint(skip: int = 0, limit: int = 100, tour_id: Optional[str] = None,
                          db: Session = Depends(get_db)):
    filters = {}
    if tour_id:
        filters['tour_id'] = tour_id
    items = list_reviews(db, skip=skip, limit=limit, filters=filters)
    return items

@router.get("/stats", response_model=ReviewStats)
def stats_endpoint(db: Session = Depends(get_db)):
    return get_stats(db)