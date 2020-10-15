import html
from unittest import TestCase

from flask_fixtures import FixturesMixin

from fyuur import create_app as init_app
from fyuur import db


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
        "fyuur/fixtures/location.json",
        "fyuur/fixtures/genres.json",
        "fyuur/fixtures/artists.json",
        "fyuur/fixtures/venues.json",
        "fyuur/fixtures/shows.json",
    ]
