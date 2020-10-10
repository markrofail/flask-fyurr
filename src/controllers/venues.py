import logging

from flask import abort, flash, jsonify, redirect, render_template, request, url_for
from flask.blueprints import Blueprint
from sqlalchemy.exc import IntegrityError

from src.forms import VenueForm
from src.models import db
from src.models.location import City
from src.models.venues import Venue

logger = logging.getLogger(__name__)
venues_views = Blueprint("venues", __name__)


# READ ----------------------------------------------------
# List
@venues_views.route("/")
def venues_list():
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    cities = City.query.filter(City.venues.any()).all()
    return render_template("pages/venues.html", cities=cities)


# Detail
@venues_views.route("/<int:venue_id>")
def venues_detail(venue_id):
    venue = Venue.query.get_or_404(venue_id)
    return render_template("pages/show_venue.html", venue=venue)


#  SEARCH -------------------------------------------------
@venues_views.route("/search", methods=["POST"])
def search_venues():
    search_term = request.form.get("search_term", "")
    venues = Venue.query.filter(Venue.name.ilike(f"%{search_term}%")).all()

    return render_template(
        "pages/search_venues.html",
        results=dict(
            count=len(venues),
            data=venues,
        ),
        search_term=search_term,
    )


#  UPDATE -------------------------------------------------
# Form GET
@venues_views.route("/<int:venue_id>/edit", methods=["GET"])
def edit_venue(venue_id):
    venue = Venue.query.get_or_404(venue_id)
    form = VenueForm(obj=venue)
    return render_template("forms/edit_venue.html", form=form, venue=venue)


# Form SUBMIT
@venues_views.route("/<int:venue_id>/edit", methods=["POST"])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    return redirect(url_for("venues.show_venue", venue_id=venue_id))


#  CREATE -------------------------------------------------
# Form GET
@venues_views.route("/create", methods=["GET"])
def create_venue_form():
    return render_template("forms/new_venue.html", form=VenueForm())


# Form SUBMIT
@venues_views.route("/create", methods=["POST"])
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
@venues_views.route("/<venue_id>", methods=["DELETE"])
def delete_venue(venue_id):
    error = False
    try:
        venue = Venue.query.get_or_404(venue_id)
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
