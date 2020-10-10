from src.models import db


class Show(db.Model):
    __tablename__ = "shows"

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)

    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), nullable=False)
    artist = db.relationship("Artist", back_populates="shows")

    venue_id = db.Column(db.Integer, db.ForeignKey("venues.id"), nullable=False)
    venue = db.relationship("Venue", back_populates="shows")

    def __repr__(self):
        return f"<Show id:{self.id} start_time:{self.start_time}>"
