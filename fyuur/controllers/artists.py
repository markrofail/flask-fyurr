import logging

from flask import Blueprint, flash, redirect, render_template, request, url_for
from sqlalchemy.exc import IntegrityError

from fyuur.forms import ArtistForm
from fyuur.models import db
from fyuur.models.artists import Artist
from fyuur.models.contact_info import ContactInfo
from fyuur.models.location import City
from fyuur.utils import flash_error, parse_errors

artists_views = Blueprint("artists", __name__)
logger = logging.getLogger(__name__)


# READ ----------------------------------------------------
# List
@artists_views.route("/", methods=["GET"])
def artists_list():
    artists = Artist.query.order_by("id").all()
    return render_template("pages/artists.html", artists=artists)


# Details
@artists_views.route("/<int:artist_id>")
def artists_detail(artist_id):
    artist = Artist.query.get_or_404(artist_id)
    return render_template("pages/show_artist.html", artist=artist)


#  SEARCH -------------------------------------------------
@artists_views.route("/search", methods=["POST"])
def search_artists():
    search_term = request.form.get("search_term", "")
    artists = Artist.query.filter(Artist.name.ilike(f"%{search_term}%")).all()

    return render_template(
        "pages/search_artists.html",
        results=dict(
            count=len(artists),
            data=artists,
        ),
        search_term=search_term,
    )


#  UPDATE -------------------------------------------------
# Form GET
@artists_views.route("/<int:artist_id>/edit", methods=["GET"])
def edit_artist(artist_id):
    artist = Artist.query.get_or_404(artist_id)
    form = ArtistForm(obj=artist)
    form.city.data = artist.city.name
    return render_template("forms/edit_artist.html", form=form, artist=artist)


# Form SUBMIT
@artists_views.route("/<int:artist_id>/edit", methods=["POST"])
def edit_artist_submission(artist_id):
    artist = Artist.query.get_or_404(artist_id)
    form = ArtistForm(request.form)
    errors = None

    if not form.validate():
        errors = parse_errors(form.errors)
        flash_error(errors)
        return render_template("forms/edit_artist.html", form=form, artist=artist)

    try:
        # create City object
        city_name, state = form.city.data, form.state.data
        city_name = city_name.strip().capitalize()

        # update city if changed
        if city_name != artist.city.name:
            city = City.query.filter_by(name=city_name).one_or_none()
            if not city:
                city = City(name=city_name, state=state)
                db.session.add(city)
            artist.city = city

        # create Contact Information object
        contact_info = artist.contact_info
        contact_info.phone = form.contact_info.phone.data
        contact_info.image_link = form.contact_info.image_link.data
        contact_info.website = form.contact_info.website.data
        contact_info.facebook_link = form.contact_info.facebook_link.data
        db.session.add(contact_info)

        artist.genres = form.genres.data
        artist.name = form.name.data.strip()
        db.session.add(artist)
        db.session.commit()

        flash(f"Artist {artist.name} was successfully updated!")
    except IntegrityError as e:
        logger.error(e)
        db.session.rollback()
        errors = True
    finally:
        db.session.close()

    if errors:
        form = ArtistForm(request.form)
        flash_error(
            f"An error occurred. Artist {request.form.get('name', '')} could not be listed"
        )
        return render_template("forms/edit_artist.html", form=form, artist=artist)
    return redirect(url_for("artists.artists_detail", artist_id=artist_id))


#  CREATE -------------------------------------------------
# Form GET
@artists_views.route("/create", methods=["GET"])
def create_artist_form():
    return render_template("forms/new_artist.html", form=ArtistForm())


# Form SUBMIT
@artists_views.route("/create", methods=["POST"])
def create_artist_submission():
    form = ArtistForm(request.form)
    errors = None

    if not form.validate():
        errors = parse_errors(form.errors)
        flash_error(errors)
        return render_template("forms/new_artist.html", form=form)

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

        # finally create Artist object
        genres = form.genres.data
        name = form.name.data.strip()

        artists = Artist(
            name=name,
            genres=genres,
            city=city,
            contact_info=contact_info,
        )
        db.session.add(artists)
        db.session.commit()

        flash(f"Artist {name} was successfully listed!")
    except IntegrityError as e:
        logger.error(e)
        db.session.rollback()
        errors = True
    finally:
        db.session.close()

    if errors:
        form = ArtistForm(request.form)
        flash_error(
            f"An error occurred. Artist {request.form.get('name', '')} could not be listed"
        )
        return render_template("forms/new_artist.html", form=form)
    return redirect(url_for("index"))
