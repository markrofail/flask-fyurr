from src.models import db
from src.models.contact_info import ContactInfo
from src.models.genres import Genres, genre_artist_assoc
from src.models.location import City
from src.models.shows import Show


class Artist(db.Model):
    __tablename__ = "artists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    genres = db.relationship(Genres, secondary=genre_artist_assoc)

    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String, nullable=True)

    # MANY artist has ONE city
    city_id = db.Column(db.Integer, db.ForeignKey("cities.id"), nullable=False)
    city = db.relationship(City, back_populates="artists")

    # ONE artist has ONE contact info
    contact_info_id = db.Column(
        db.Integer, db.ForeignKey("contact_info.id"), nullable=False, unique=True
    )
    contact_info = db.relationship(
        ContactInfo, uselist=False, cascade="all, delete-orphan", single_parent=True
    )

    # ONE artist has MANY shows
    shows = db.relationship(Show, back_populates="artist", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Artist name:{self.name}>"
