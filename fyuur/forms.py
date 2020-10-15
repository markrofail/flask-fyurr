import re
from datetime import datetime
from urllib.parse import urlparse

from flask_wtf import FlaskForm
from wtforms import DateTimeField, FormField, StringField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import URL, DataRequired, ValidationError, optional

from fyuur.models import db
from fyuur.models.genres import Genres
from fyuur.models.location import State


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
    def validate_facebook(self, field):
        if field.data:
            test_string = field.data
            if not test_string.startswith("http"):
                test_string = "http://" + test_string

            parsed_uri = urlparse(test_string)
            if not (
                parsed_uri.netloc.startswith("facebook")
                or parsed_uri.netloc.startswith("www.facebook")
            ):
                raise ValidationError("Not a facebook link")

    def validate_phone(self, phone):
        if phone.data:
            reg = re.compile(r"\d{3}-\d{3}-\d{4}")
            assert reg.match(phone.data)

    phone = StringField("phone", validators=[DataRequired(), validate_phone])
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
