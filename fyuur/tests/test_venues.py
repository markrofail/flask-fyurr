from flask import url_for

from fyuur.models.venues import Venue

from .conftest import FlaskTestCase, decode_response


class TestVenues(FlaskTestCase):
    def test_list(self):
        """
        Test Venue List: test that all venues are listed in /venues/
        """
        venues = Venue.query.all()

        response = self.client.get(url_for("venues.venues_list"))
        response_data = decode_response(response)

        for venue in venues:
            self.assertIn(venue.name, response_data)

    def test_detail(self):
        """
        Test Venue Detail: test that all venue details are listed in /venues/<venue_id>
        """
        response = self.client.get(url_for("venues.venues_detail", venue_id=199))
        response_data = decode_response(response)

        # assert name, address
        self.assertIn("The Musical Hop", response_data)
        self.assertIn("1015 Folsom Street", response_data)

        # assert past and upcoming shows
        self.assertIn("0 Upcoming Shows", response_data)
        self.assertIn("1 Past Show", response_data)

    def test_search(self):
        """
        Test Venue Search: test that all matching venues are listed in /venues/search
        """

        # search for Hop should return "The Musical Hop".
        response = self.client.post(
            url_for("venues.search_venues"), data=dict(search_term="Hop")
        )
        response_data = decode_response(response)
        self.assertIn("The Musical Hop", response_data)

        # should be case insensitive
        response = self.client.post(
            url_for("venues.search_venues"), data=dict(search_term="hOP")
        )
        response_data = decode_response(response)
        self.assertIn("The Musical Hop", response_data)

        # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
        response = self.client.post(
            url_for("venues.search_venues"), data=dict(search_term="Music")
        )
        response_data = decode_response(response)
        self.assertIn("The Musical Hop", response_data)
        self.assertIn("Park Square Live Music & Coffee", response_data)

    def test_edit(self):
        """
        Test Venue Edit: test that a venue can be edited /venues/<venue_id>/edit
        """
        venue = Venue.query.get(199)

        payload = {
            "city": venue.city.name,
            "state": venue.city.state.id,
            "contact_info-phone": venue.contact_info.phone,
            "contact_info-image_link": venue.contact_info.image_link,
            "contact_info-website": venue.contact_info.website,
            "contact_info-facebook_link": venue.contact_info.facebook_link,
            "genres": [x.id for x in venue.genres],
            "name": venue.name,
            "address": venue.address,
        }

        # edit one thing
        payload["name"] = "A New Name"

        self.client.post(
            url_for("venues.edit_venue_submission", venue_id=199), data=payload
        )

        venue = Venue.query.get(199)
        self.assertEqual(venue.name, "A New Name")

    def test_create(self):
        """
        Test Venue Create: test that a venue can be created /venues/create
        """

        payload = {
            "city": "Alexandria",
            "state": 1,
            "contact_info-phone": "111-222-3333",
            "contact_info-image_link": None,
            "contact_info-website": None,
            "contact_info-facebook_link": None,
            "genres": [1],
            "name": "A Brand New Name",
            "address": "Alexandria Road",
        }

        self.client.post(url_for("venues.create_venue_submission"), data=payload)

        venue = Venue.query.get(199)

        self.assertEqual(venue.name, payload["name"])
        self.assertEqual(venue.city.state.id, payload["state"])
        self.assertEqual(venue.contact_info.phone, payload["contact_info-phone"])
        self.assertEqual(venue.genres[0].id, payload["genres"][0])
        self.assertEqual(venue.address, payload["address"])

    def test_delete(self):
        """
        Test Venue Delete: test that a venue can be delete /venues/<venue_id>
        """
        self.assertEqual(Venue.filter_by(id=199).all(), 1)

        self.client.delete(url_for("venues.delete_venue", venue_id=199))

        self.assertEqual(Venue.filter_by(id=199).all(), 0)
