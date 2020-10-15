from flask import url_for

from fyuur.models.artists import Artist

from .conftest import FlaskTestCase, decode_response


class TestArtists(FlaskTestCase):
    def test_list(self):
        """
        Test Artist List: test that all artists are listed in /artists/
        """
        artists = Artist.query.all()

        response = self.client.get(url_for("artists.artists_list"))
        response_data = decode_response(response)

        for artist in artists:
            self.assertIn(artist.name, response_data)

    def test_detail(self):
        """
        Test Artist Detail: test that all artist details are listed in /artists/<artist_id>
        """
        response = self.client.get(url_for("artists.artists_detail", artist_id=99))
        response_data = decode_response(response)

        # assert name
        self.assertIn("Guns N Petals", response_data)

        # assert past and upcoming shows
        self.assertIn("0 Upcoming Shows", response_data)
        self.assertIn("1 Past Show", response_data)

    def test_search(self):
        """
        Test Artist Search: test that all matching artists are listed in /artist/search
        """

        # search for band should return "The Wild Sax Band".
        response = self.client.post(
            url_for("artists.search_artists"), data=dict(search_term="band")
        )
        response_data = decode_response(response)
        self.assertIn("The Wild Sax Band", response_data)

        # should be case insensitive
        response = self.client.post(
            url_for("artists.search_artists"), data=dict(search_term="bAnD")
        )
        response_data = decode_response(response)
        self.assertIn("The Wild Sax Band", response_data)

        # search for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
        response = self.client.post(
            url_for("artists.search_artists"), data=dict(search_term="A")
        )
        response_data = decode_response(response)
        self.assertIn("Guns N Petals", response_data)
        self.assertIn("Matt Quevedo", response_data)
        self.assertIn("The Wild Sax Band", response_data)

    def test_edit(self):
        """
        Test Artist Edit: test that an artist can be edited /artist/<artist_id>/edit
        """
        artist = Artist.query.get(99)

        payload = {
            "city": artist.city.name,
            "state": artist.city.state.id,
            "contact_info-phone": artist.contact_info.phone,
            "contact_info-image_link": artist.contact_info.image_link,
            "contact_info-website": artist.contact_info.website,
            "contact_info-facebook_link": artist.contact_info.facebook_link,
            "genres": [x.id for x in artist.genres],
            "name": artist.name,
        }

        # edit one thing
        payload["name"] = "A New Name"

        self.client.post(
            url_for("artists.edit_artist_submission", artist_id=99), data=payload
        )

        artist = Artist.query.get(99)
        self.assertEqual(artist.name, "A New Name")

    def test_create(self):
        """
        Test Artist Create: test that an artist can be created /artists/create
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
        }

        self.client.post(url_for("artists.create_artist_submission"), data=payload)

        artist = Artist.query.get(1)

        self.assertEqual(artist.name, payload["name"])
        self.assertEqual(artist.city.state.id, payload["state"])
        self.assertEqual(artist.contact_info.phone, payload["contact_info-phone"])
        self.assertEqual(artist.genres[0].id, payload["genres"][0])
