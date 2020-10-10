from src.models import db


class State(db.Model):
    __tablename__ = "states"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # ONE state has MANY cities
    cities = db.relationship("City")

    def __repr__(self):
        return f"<State name:{self.name}>"


class City(db.Model):
    __tablename__ = "cities"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # MANY city have ONE state
    state_id = db.Column(db.Integer, db.ForeignKey("states.id"))
    state = db.relationship("State", back_populates="cities", lazy="joined")

    # ONE city has MANY venues
    venues = db.relationship("Venue")

    # ONE city has MANY artists
    artists = db.relationship("Artist")

    def __repr__(self):
        return f"<City name:{self.name} state:{self.state}>"
