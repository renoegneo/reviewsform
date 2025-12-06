from typing import Dict, Optional, Sequence
from sqlalchemy.orm import Session
from sqlalchemy import func, select, and_

from app.models import Review
from app.schemas import ReviewCreate


def create_review(db: Session, review_in: ReviewCreate) -> Review:

    overall = (
        review_in.vehicle
        + review_in.driver
        + review_in.guide
        + review_in.accommodation
        + review_in.meals
    ) / 5.0

    obj = Review(
        vehicle=review_in.vehicle,
        driver=review_in.driver,
        guide=review_in.guide,
        accommodation=review_in.accommodation,
        meals=review_in.meals,
        comment=review_in.comment,
        name=review_in.name,
        email=review_in.email,
        tour_id=review_in.tour_id,
        overall_score=overall,
    )

    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def list_reviews(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    filters: Optional[Dict] = None
) -> Sequence[Review]:
    stmt = select(Review).order_by(Review.created_at.desc()).offset(skip).limit(limit)

    if filters:
        conditions = []
        min_score = filters.get("min_score")
        if min_score is not None:
            conditions.append(Review.overall_score >= min_score)

        tour_id = filters.get("tour_id")
        if tour_id:
            conditions.append(Review.tour_id == tour_id)

        from_date = filters.get("from_date")
        if from_date:
            conditions.append(Review.created_at >= from_date)

        to_date = filters.get("to_date")
        if to_date:
            conditions.append(Review.created_at <= to_date)

        if conditions:
            stmt = stmt.where(and_(*conditions))

    results = db.scalars(stmt).all()  # -> List[Review]
    return results


def get_stats(db: Session) -> Dict:

    total = db.query(func.count(Review.id)).scalar() or 0

    avg_vehicle = db.query(func.avg(Review.vehicle)).scalar() or 0
    avg_driver = db.query(func.avg(Review.driver)).scalar() or 0
    avg_guide = db.query(func.avg(Review.guide)).scalar() or 0
    avg_accom = db.query(func.avg(Review.accommodation)).scalar() or 0
    avg_meals = db.query(func.avg(Review.meals)).scalar() or 0
    avg_overall = db.query(func.avg(Review.overall_score)).scalar() or 0
    dist_vehicle = {
        str(k): int(v)
        for k, v in (
            db.query(Review.vehicle, func.count(Review.vehicle))
            .group_by(Review.vehicle)
            .all()
        )
    }

    return {
        "total": total,
        "averages": {
            "vehicle": float(avg_vehicle),
            "driver": float(avg_driver),
            "guide": float(avg_guide),
            "accommodation": float(avg_accom),
            "meals": float(avg_meals),
            "overall": float(avg_overall),
        },
        "distribution": {
            "vehicle": dist_vehicle
        },
    }
