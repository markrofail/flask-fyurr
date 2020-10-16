import datetime

from sqlalchemy.ext.hybrid import hybrid_property

from fyyur.models import PkModelMixin, db
from fyyur.models.contact_info import ContactInfo
from fyyur.models.genres import Genres, genre_artist_assoc
from fyyur.models.location import City
from fyyur.models.shows import Show


class Artist(PkModelMixin, db.Model):
    __tablename__ = "artists"

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

    @hybrid_property
    def upcoming_shows(self):
        today = datetime.date.today()
        return Show.query.filter(
            Show.artist_id == self.id, Show.start_time >= today
        ).all()

    @hybrid_property
    def upcoming_shows_count(self):
        today = datetime.date.today()
        return Show.query.filter(
            Show.artist_id == self.id, Show.start_time >= today
        ).count()

    @hybrid_property
    def past_shows(self):
        today = datetime.date.today()
        return Show.query.filter(
            Show.artist_id == self.id, Show.start_time < today
        ).all()

    @hybrid_property
    def past_shows_count(self):
        today = datetime.date.today()
        return Show.query.filter(
            Show.artist_id == self.id, Show.start_time < today
        ).count()
