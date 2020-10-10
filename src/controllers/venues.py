import logging

from flask import abort, flash, jsonify, redirect, render_template, request, url_for
from flask.blueprints import Blueprint
from sqlalchemy.exc import IntegrityError

from src.forms import VenueForm
from src.models import db
from src.models.venues import Venue

logger = logging.getLogger(__name__)
venues_api = Blueprint("venues_api", __name__)


# READ ----------------------------------------------------
# List
@venues_api.route("/")
def venues_list():
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    data = [
        {
            "city": "San Francisco",
            "state": "CA",
            "venues": [
                {
                    "id": 1,
                    "name": "The Musical Hop",
                    "num_upcoming_shows": 0,
                },
                {
                    "id": 3,
                    "name": "Park Square Live Music & Coffee",
                    "num_upcoming_shows": 1,
                },
            ],
        },
        {
            "city": "New York",
            "state": "NY",
            "venues": [
                {
                    "id": 2,
                    "name": "The Dueling Pianos Bar",
                    "num_upcoming_shows": 0,
                }
            ],
        },
    ]
    return render_template("pages/venues.html", areas=data)


# Detail
@venues_api.route("/<int:venue_id>")
def venues_detail(venue_id):
    venue = Venue.query.get(venue_id)
    return render_template("pages/show_venue.html", venue=venue)


#  SEARCH -------------------------------------------------
@venues_api.route("/search", methods=["POST"])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # search for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    response = {
        "count": 1,
        "data": [
            {
                "id": 2,
                "name": "The Dueling Pianos Bar",
                "num_upcoming_shows": 0,
            }
        ],
    }
    return render_template(
        "pages/search_venues.html",
        results=response,
        search_term=request.form.get("search_term", ""),
    )


#  UPDATE -------------------------------------------------
# Form GET
@venues_api.route("/<int:venue_id>/edit", methods=["GET"])
def edit_venue(venue_id):
    venue = Venue.query.get(venue_id)
    return render_template("forms/edit_venue.html", form=VenueForm(), venue=venue)


# Form SUBMIT
@venues_api.route("/<int:venue_id>/edit", methods=["POST"])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    return redirect(url_for("venues_api.show_venue", venue_id=venue_id))


#  CREATE -------------------------------------------------
# Form GET
@venues_api.route("/create", methods=["GET"])
def create_venue_form():
    return render_template("forms/new_venue.html", form=VenueForm())


# Form SUBMIT
@venues_api.route("/create", methods=["POST"])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    # on successful db insert, flash success
    flash("Venue " + request.form["name"] + " was successfully listed!")
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template("pages/home.html")


#  DELETE -------------------------------------------------
@venues_api.route("/<venue_id>", methods=["DELETE"])
def delete_venue(venue_id):
    error = False
    try:
        venue = Venue.query.get(venue_id)
        db.session.delete(venue)
        db.session.commit()
    except IntegrityError as e:
        logger.error(e)
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return jsonify({"success": True})
    return None
