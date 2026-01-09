from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()

class Person(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    height: Mapped[int] = mapped_column(nullable=False)
    birth_year: Mapped[str] = mapped_column(String(7), nullable=False)
    favorites: Mapped[List["Favorite"]] = relationship(back_populates="person")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "birth_year": self.birth_year,
        }

class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    terrain: Mapped[str] = mapped_column(String(50), nullable=False)
    population: Mapped[int] = mapped_column(nullable=False)
    favorites: Mapped[List["Favorite"]] = relationship(back_populates="planet")

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "terrain": self.terrain,
            "population": self.population
        }

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(20), nullable=False)
    last_name: Mapped[str] = mapped_column(String(40), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    favorites: Mapped[List["Favorite"]] = relationship(back_populates="user")

    def serialize(self):
        return{
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }
    
class Favorite(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    planet_id: Mapped[int | None] = mapped_column(ForeignKey("planet.id"), nullable=True)
    planet: Mapped["Planet"] = relationship(back_populates="favorites")
    person_id: Mapped[int | None] = mapped_column(ForeignKey("person.id"), nullable=True)
    person: Mapped["Person"] = relationship(back_populates="favorites")
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="favorites")

    def serialize(self):
        return{
            "id": self.id,
            "planet_id": self.planet_id,
            "person_id": self.person_id,
            "user_id": self.user_id
        }