from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Integer, Float, DateTime
from sqlalchemy.sql import func

from .db import Base


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    vehicle: Mapped[int] = mapped_column(Integer, nullable=False)
    driver: Mapped[int] = mapped_column(Integer, nullable=False)
    guide: Mapped[int] = mapped_column(Integer, nullable=False)
    accommodation: Mapped[int] = mapped_column(Integer, nullable=False)
    meals: Mapped[int] = mapped_column(Integer, nullable=False)

    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    email: Mapped[str | None] = mapped_column(String(200), nullable=True)
    tour_id: Mapped[str | None] = mapped_column(String(100), nullable=True)

    overall_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    created_at: Mapped[str] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
