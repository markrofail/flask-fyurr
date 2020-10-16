import datetime

from flask import url_for

from fyyur.models.shows import Show

from .conftest import FlaskTestCase, decode_response


class TestShows(FlaskTestCase):
    def test_list(self):
        """
        Test Show List: test that all shows are listed in /shows/
        """
        shows = Show.query.all()

        response = self.client.get(url_for("shows.shows_list"))
        response_data = decode_response(response)

        for show in shows:
            self.assertIn(str(show.start_time), response_data)

    def test_create(self):
        """
        Test Show Create: test that a show can be created /shows/create
        """

        today = datetime.datetime.now().replace(microsecond=0)
        payload = {
            "start_time": today.strftime("%Y-%m-%d %H:%M:%S"),
            "venue_id": 99,
            "artist_id": 199,
        }

        self.client.post(url_for("shows.create_show_submission"), data=payload)

        show = Show.query.get(1)

        self.assertEqual(show.start_time, today)
        self.assertEqual(show.venue_id, payload["venue_id"])
        self.assertEqual(show.artist_id, payload["artist_id"])
