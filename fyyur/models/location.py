from fyyur.models import PkModelMixin, db


class State(PkModelMixin, db.Model):
    __tablename__ = "states"
    name = db.Column(db.String)

    # ONE state has MANY cities
    cities = db.relationship("City")

    def __repr__(self):
        return f"<State name:{self.name}>"


class City(PkModelMixin, db.Model):
    __tablename__ = "cities"
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
