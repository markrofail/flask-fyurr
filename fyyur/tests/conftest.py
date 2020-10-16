import html
from unittest import TestCase

from flask_fixtures import FixturesMixin

from fyyur import create_app as init_app
from fyyur import db


def decode_response(response):
    decoded_resp = response.data.decode("utf-8")
    unescaped_resp = html.unescape(decoded_resp)
    return unescaped_resp


class FlaskTestCase(TestCase, FixturesMixin):
    app = init_app("settings:test")
    client = app.test_client()
    db = db

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    fixtures = [
        "fyyur/fixtures/location.json",
        "fyyur/fixtures/genres.json",
        "fyyur/fixtures/artists.json",
        "fyyur/fixtures/venues.json",
        "fyyur/fixtures/shows.json",
    ]
