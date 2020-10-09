from src.models import db

shows = db.Table(
    "shows",
    db.Column("artist_id", db.Integer, db.ForeignKey("artists.id"), primary_key=True),
    db.Column("venue_id", db.Integer, db.ForeignKey("venues.id"), primary_key=True),
    db.Column("start_time", db.DateTime, nullable=False),
)
