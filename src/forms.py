from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import DateTimeField, FormField, StringField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import URL, DataRequired, optional
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


class ContactInfoForm(FlaskForm):
    def validate_facebook(form, field):
        if field.data:
            return (
                field.data.startswith("facebook.com")
                or field.data.startswith("http://facebook.com")
                or field.data.startswith("https:/facebook.com")
            )

    phone = PhoneNumberField("phone", display_format="international", region=None)
    image_link = StringField("image_link")
    website = StringField("website")
    facebook_link = StringField(
        "facebook_link", validators=[optional(), URL(), validate_facebook]
    )


class VenueForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    address = StringField("address", validators=[DataRequired()])

    city = StringField("city", validators=[DataRequired()])
    state = QuerySelectField(
        "state",
        validators=[DataRequired()],
        query_factory=state_choices,
        get_label="name",
    )

    genres = QuerySelectMultipleField(
        "genres",
        validators=[DataRequired()],
        query_factory=genre_choices,
        get_label="name",
    )

    contact_info = FormField(ContactInfoForm)


class ArtistForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])

    city = StringField("city", validators=[DataRequired()])
    state = QuerySelectField(
        "state",
        validators=[DataRequired()],
        query_factory=state_choices,
        get_label="name",
    )

    genres = QuerySelectMultipleField(
        "genres",
        validators=[DataRequired()],
        query_factory=genre_choices,
        get_label="name",
    )

    contact_info = FormField(ContactInfoForm)
