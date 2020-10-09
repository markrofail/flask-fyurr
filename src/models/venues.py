from src.models import db
from src.models.shows import shows


class Venue(db.Model):
    __tablename__ = "venues"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    shows = db.relationship(
        "artists",
        secondary=shows,
        lazy="subquery",
        backref=db.backref("artists", lazy=True),
    )
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
