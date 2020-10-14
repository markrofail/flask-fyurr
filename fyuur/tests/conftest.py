from unittest import TestCase

from flask_fixtures import FixturesMixin

from fyuur import create_app as init_app
from fyuur import db


class FlaskTestCase(TestCase, FixturesMixin):
    app = init_app("settings:test")
    client = app.test_client()
    db = db

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
