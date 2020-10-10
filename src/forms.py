from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import DateTimeField, StringField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import URL, DataRequired
from wtforms_alchemy import PhoneNumberField

from src.models import db
from src.models.genres import Genres
from src.models.location import State


def state_choices():
    return db.session.query(State).all()


def genre_choices():
    return db.session.query(Genres).all()


class ShowForm(FlaskForm):
    artist_id = StringField("artist_id")
    venue_id = StringField("venue_id")
    start_time = DateTimeField(
        "start_time", validators=[DataRequired()], default=datetime.today()
    )


class VenueForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    city = StringField("city", validators=[DataRequired()])
    state = QuerySelectField(
        "state",
        validators=[DataRequired()],
        query_factory=state_choices,
        get_label="name",
    )
    address = StringField("address", validators=[DataRequired()])
    phone = PhoneNumberField("phone", display_format="national")
    image_link = StringField("image_link")
    genres = QuerySelectMultipleField(
        "genres",
        validators=[DataRequired()],
        query_factory=genre_choices,
        get_label="name",
    )
    facebook_link = StringField("facebook_link", validators=[URL()])


class ArtistForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    city = StringField("city", validators=[DataRequired()])
    state = QuerySelectField(
        "state",
        validators=[DataRequired()],
        query_factory=state_choices,
        get_label="name",
    )
    phone = PhoneNumberField("phone", display_format="national")
    image_link = StringField("image_link")
    genres = QuerySelectMultipleField(
        "genres",
        validators=[DataRequired()],
        query_factory=genre_choices,
        get_label="name",
    )
    facebook_link = StringField(
        # TODO implement enum restriction
        "facebook_link",
        validators=[URL()],
    )


# TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM
