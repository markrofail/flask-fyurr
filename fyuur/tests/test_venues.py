import html

from flask import url_for

from fyuur.models.venues import Venue

from .conftest import FlaskTestCase


def _decode_response(response):
    decoded_resp = response.data.decode("utf-8")
    unescaped_resp = html.unescape(decoded_resp)
    return unescaped_resp


class TestVenues(FlaskTestCase):

    fixtures = [
        "fyuur/fixtures/location.json",
        "fyuur/fixtures/genres.json",
        "fyuur/fixtures/venues.json",
    ]

    def test_list(self):
        """
        Test Venue List: test that all venues are listed in /venues/
        """
        venues = Venue.query.all()

        response = self.client.get(url_for("venues.venues_list"))
        response_data = _decode_response(response)

        for venue in venues:
            self.assertIn(venue.name, response_data)

    def test_detail(self):
        """
        Test Venue Detail: test that all venue details are listed in /venues/<venue_id>
        """
        venue = Venue.query.get(1)

        response = self.client.get(url_for("venues.venues_detail", venue_id=1))
        response_data = _decode_response(response)

        # assert name, address
        self.assertIn(venue.name, response_data)

        # assert past and upcoming shows
        self.assertIn(f"{venue.upcoming_shows_count} Upcoming Shows", response_data)
        self.assertIn(f"{venue.past_shows_count} Past Shows", response_data)

    def test_search(self):
        """
        Test Venue Search: test that all matching venues are listed in /venues/search
        """
