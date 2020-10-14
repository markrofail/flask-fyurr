import logging

from flask import abort, flash, jsonify, redirect, render_template, request, url_for
from flask.blueprints import Blueprint
from sqlalchemy.exc import IntegrityError

from fyuur.forms import VenueForm
from fyuur.models import db
from fyuur.models.contact_info import ContactInfo
from fyuur.models.location import City
from fyuur.models.venues import Venue
from fyuur.utils import flash_error, parse_errors

logger = logging.getLogger(__name__)
venues_views = Blueprint("venues", __name__)


# READ ----------------------------------------------------
# List
@venues_views.route("/")
def venues_list():
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
    form.city.data = venue.city.name
    return render_template("forms/edit_venue.html", form=form, venue=venue)


# Form SUBMIT
@venues_views.route("/<int:venue_id>/edit", methods=["POST"])
def edit_venue_submission(venue_id):
    venue = Venue.query.get_or_404(venue_id)
    form = VenueForm(request.form)
    errors = None

    if not form.validate():
        errors = parse_errors(form.errors)
        flash_error(errors)
        return render_template("forms/edit_venue.html", form=form, venue=venue)

    try:
        # create City object
        city_name, state = form.city.data, form.state.data
        city_name = city_name.strip().capitalize()

        # update city if changed
        if city_name != venue.city.name:
            city = City.query.filter_by(name=city_name).one_or_none()
            if not city:
                city = City(name=city_name, state=state)
                db.session.add(city)
            venue.city = city

        # create Contact Information object
        contact_info = venue.contact_info
        contact_info.phone = form.contact_info.phone.data
        contact_info.image_link = form.contact_info.image_link.data
        contact_info.website = form.contact_info.website.data
        contact_info.facebook_link = form.contact_info.facebook_link.data
        db.session.add(contact_info)

        # finally create Venue object
        venue.genres = form.genres.data
        venue.name = form.address.data.strip()
        venue.address = form.address.data.strip()
        db.session.add(venue)
        db.session.commit()

        flash(f"Venue {venue.name} was successfully listed!")
    except IntegrityError as e:
        logger.error(e)
        db.session.rollback()
        errors = True
    finally:
        db.session.close()

    if errors:
        form = VenueForm(request.form)
        flash_error(
            f"An error occurred. Venue {request.form.get('name', '')} could not be listed"
        )
        return render_template("forms/edit_venue.html", form=form, venue=venue)
    return redirect(url_for("venues.venues_detail", venue_id=venue_id))


#  CREATE -------------------------------------------------
# Form GET
@venues_views.route("/create", methods=["GET"])
def create_venue_form():
    return render_template("forms/new_venue.html", form=VenueForm())


# Form SUBMIT
@venues_views.route("/create", methods=["POST"])
def create_venue_submission():
    form = VenueForm(request.form)
    errors = None

    if not form.validate():
        errors = parse_errors(form.errors)
        flash_error(errors)
        return render_template("forms/new_venue.html", form=form)

    try:
        # create City object
        city_name, state = form.city.data, form.state.data
        city_name = city_name.strip().capitalize()

        # get or create
        city = City.query.filter_by(name=city_name).one_or_none()
        if not city:
            city = City(name=city_name, state=state)
            db.session.add(city)

        # create Contact Information object
        contact_info = ContactInfo(
            phone=form.contact_info.phone.data,
            image_link=form.contact_info.image_link.data,
            website=form.contact_info.website.data,
            facebook_link=form.contact_info.facebook_link.data,
        )
        db.session.add(contact_info)

        # finally create Venue object
        genres = form.genres.data
        address = form.address.data.strip()
        name = form.name.data.strip()

        venue = Venue(
            name=name,
            address=address,
            genres=genres,
            city=city,
            contact_info=contact_info,
        )
        db.session.add(venue)
        db.session.commit()

        flash(f"Venue {name} was successfully listed!")
    except IntegrityError as e:
        logger.error(e)
        db.session.rollback()
        errors = True
    finally:
        db.session.close()

    if errors:
        form = VenueForm(request.form)
        flash_error(
            f"An error occurred. Venue {request.form.get('name', '')} could not be listed"
        )
        return render_template("forms/new_venue.html", form=form)
    return redirect(url_for("index"))


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
