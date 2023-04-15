import datetime

from sqlalchemy import String, DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


class Base(DeclarativeBase):
    ...


class PivniValka(Base):
    __tablename__ = "pivni_valka"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    date: Mapped[datetime.datetime] = mapped_column(DateTime())
    user: Mapped[str] = mapped_column(String())
    unique_beers: Mapped[int] = mapped_column(Integer())
