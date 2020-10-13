from src.models import PkModelMixin, db


class Genres(PkModelMixin, db.Model):
    __tablename__ = "genres"
    name = db.Column(db.String)

    def __repr__(self):
        return f"<Genre name:{self.name}>"


genre_artist_assoc = db.Table(
    "genre_artist_assoc",
    db.Column("genre_id", db.Integer, db.ForeignKey("genres.id")),
    db.Column("artist_id", db.Integer, db.ForeignKey("artists.id")),
)

genre_venue_assoc = db.Table(
    "genre_venue_assoc",
    db.Column("genre_id", db.Integer, db.ForeignKey("genres.id")),
    db.Column("venue_id", db.Integer, db.ForeignKey("venues.id")),
)
