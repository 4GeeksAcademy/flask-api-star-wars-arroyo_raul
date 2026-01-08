from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()

class Person(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    height: Mapped[int] = mapped_column(nullable=False)
    birth_year: Mapped[str] = mapped_column(String(7), nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "birth_year": self.birth_year,
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    terrain: Mapped[str] = mapped_column(String(50), nullable=False)
    population: Mapped[int] = mapped_column(nullable=False)

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

    def serialize(self):
        return{
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }
    
class Favorite(db.Model):
    id: Mapped[int] = mapped_column(primery_key=True, autoincrement=True)
    