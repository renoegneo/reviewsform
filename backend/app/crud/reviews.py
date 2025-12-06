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
    """
    Возвращает статистику для dashboard:
    - Общее количество отзывов
    - Средние оценки по всем категориям
    - Распределение оценок (для графиков)
    """

    # Общее количество
    total = db.query(func.count(Review.id)).scalar() or 0

    # Средние значения
    avg_vehicle = db.query(func.avg(Review.vehicle)).scalar() or 0
    avg_driver = db.query(func.avg(Review.driver)).scalar() or 0
    avg_guide = db.query(func.avg(Review.guide)).scalar() or 0
    avg_accom = db.query(func.avg(Review.accommodation)).scalar() or 0
    avg_meals = db.query(func.avg(Review.meals)).scalar() or 0
    avg_overall = db.query(func.avg(Review.overall_score)).scalar() or 0

    # Распределение оценок для ВСЕХ категорий (для графиков)
    def get_distribution(column):
        """Helper функция для подсчёта распределения"""
        result = (
            db.query(column, func.count(column))
            .group_by(column)
            .all()
        )
        # Превращаем в словарь {оценка: количество}
        # Заполняем все оценки 1-4, даже если их нет (для красивых графиков)
        dist = {1: 0, 2: 0, 3: 0, 4: 0}
        for rating, count in result:
            dist[rating] = int(count)
        return dist

    dist_vehicle = get_distribution(Review.vehicle)
    dist_driver = get_distribution(Review.driver)
    dist_guide = get_distribution(Review.guide)
    dist_accommodation = get_distribution(Review.accommodation)
    dist_meals = get_distribution(Review.meals)

    return {
        "total": total,
        "averages": {
            "vehicle": round(float(avg_vehicle), 2),
            "driver": round(float(avg_driver), 2),
            "guide": round(float(avg_guide), 2),
            "accommodation": round(float(avg_accom), 2),
            "meals": round(float(avg_meals), 2),
            "overall": round(float(avg_overall), 2),
        },
        "distribution": {
            "vehicle": dist_vehicle,
            "driver": dist_driver,
            "guide": dist_guide,
            "accommodation": dist_accommodation,
            "meals": dist_meals,
        },
    }
