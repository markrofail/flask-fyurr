from src.models import db
from src.models.contact_info import ContactInfo
from src.models.location import City


class Artist(db.Model):
    __tablename__ = "artists"

    id = db.Column(db.Integer, primary_key=True)
    genres = db.Column(db.String(120))
    name = db.Column(db.String)

    # MANY artist has ONE city
    city_id = db.Column(db.Integer, db.ForeignKey("cities.id"), nullable=False)
    city = db.relationship(City, back_populates="artists")

    # ONE artist has ONE contact info
    contact_info_id = db.Column(
        db.Integer, db.ForeignKey("contact_info.id"), nullable=False, unique=True
    )
    contact_info = db.relationship(ContactInfo, uselist=False)
