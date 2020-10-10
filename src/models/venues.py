from src.models import db
from src.models.contact_info import ContactInfo
from src.models.location import City
from src.models.shows import Shows


class Venue(db.Model):
    __tablename__ = "venues"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String(120))

    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String, nullable=True)

    # MANY venues has ONE city
    city_id = db.Column(db.Integer, db.ForeignKey("cities.id"), nullable=False)
    city = db.relationship(City, back_populates="venues")

    # ONE venues has ONE contact info
    contact_info_id = db.Column(
        db.Integer, db.ForeignKey("contact_info.id"), nullable=False, unique=True
    )
    contact_info = db.relationship(ContactInfo, uselist=False)

    # MANY artists have MANY venues
    shows = db.relationship(
        "Artist",
        secondary=Shows,
        lazy="subquery",
        backref=db.backref("venues", lazy=True),
    )
