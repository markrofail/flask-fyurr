import datetime

from sqlalchemy.ext.hybrid import hybrid_property

from fyyur.models import PkModelMixin, db
from fyyur.models.contact_info import ContactInfo
from fyyur.models.genres import Genres, genre_venue_assoc
from fyyur.models.location import City
from fyyur.models.shows import Show


class Venue(PkModelMixin, db.Model):
    __tablename__ = "venues"

    name = db.Column(db.String)
    address = db.Column(db.String(120))

    genres = db.relationship(Genres, secondary=genre_venue_assoc)

    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String, nullable=True)

    # MANY venues has ONE city
    city_id = db.Column(db.Integer, db.ForeignKey("cities.id"), nullable=False)
    city = db.relationship(City, back_populates="venues")

    # ONE venues has ONE contact info
    contact_info_id = db.Column(
        db.Integer, db.ForeignKey("contact_info.id"), nullable=False, unique=True
    )
    contact_info = db.relationship(
        ContactInfo, uselist=False, cascade="all, delete-orphan", single_parent=True
    )

    # ONE venue has MANY shows
    shows = db.relationship(Show, back_populates="venue", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Venue name:{self.name}>"

    @hybrid_property
    def upcoming_shows(self):
        today = datetime.date.today()
        return Show.query.filter(
            Show.venue_id == self.id, Show.start_time >= today
        ).all()

    @hybrid_property
    def upcoming_shows_count(self):
        today = datetime.date.today()
        return Show.query.filter(
            Show.venue_id == self.id, Show.start_time >= today
        ).count()

    @hybrid_property
    def past_shows(self):
        today = datetime.date.today()
        return Show.query.filter(
            Show.venue_id == self.id, Show.start_time < today
        ).all()

    @hybrid_property
    def past_shows_count(self):
        today = datetime.date.today()
        return Show.query.filter(
            Show.venue_id == self.id, Show.start_time < today
        ).count()
