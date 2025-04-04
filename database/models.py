import datetime

from sqlalchemy import Date, DateTime, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase): ...


class PivniValka(Base):
    __tablename__ = "pivni_valka"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    date: Mapped[datetime.date] = mapped_column(Date())
    user: Mapped[str] = mapped_column(String())
    unique_beers: Mapped[int] = mapped_column(Integer())

    def __repr__(self) -> str:
        return (
            f"PivniValka("
            f"id={self.id!r}, "
            f"date={self.date!r}, "
            f"user={self.user!r}, "
            f"unique_beers={self.unique_beers!r}"
            f")"
        )


class Archive(Base):
    __tablename__ = "archive"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    dt_utc: Mapped[datetime.datetime] = mapped_column(DateTime())
    user: Mapped[str] = mapped_column(String())
    beer: Mapped[str] = mapped_column(String())
    brewery: Mapped[str] = mapped_column(String())
    venue: Mapped[str | None] = mapped_column(String())

    def __repr__(self) -> str:
        return (
            f"Archive("
            f"id={self.id!r}, "
            f"dt_utc={self.dt_utc!r}, "
            f"user={self.user!r}, "
            f"beer={self.beer!r}, "
            f"brewery={self.brewery!r}, "
            f"venue={self.venue!r}"
            f")"
        )
