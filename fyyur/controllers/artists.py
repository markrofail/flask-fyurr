import datetime
import logging

from flask import Blueprint, flash, redirect, render_template, request, url_for
from sqlalchemy.exc import IntegrityError

from fyyur.forms import ArtistForm
from fyyur.models import db
from fyyur.models.artists import Artist
from fyyur.models.contact_info import ContactInfo
from fyyur.models.location import City
from fyyur.models.shows import Show
from fyyur.utils import flash_error, parse_errors

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

    upcoming_shows = (
        db.session.query(Show)
        .join(Artist)
        .filter(Show.artist_id == artist_id, Show.start_time >= datetime.datetime.now())
        .all()
    )

    past_shows = (
        db.session.query(Show)
        .join(Artist)
        .filter(Show.artist_id == artist_id, Show.start_time < datetime.datetime.now())
        .all()
    )

    shows_info = dict(
        past_shows=past_shows,
        upcoming_shows=upcoming_shows,
        past_shows_count=len(past_shows),
        upcoming_shows_count=len(upcoming_shows),
    )

    return render_template("pages/show_artist.html", artist=artist, **shows_info)


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
    return render_template("forms/edit_artist.html", form=form, artist=artist)


# Form SUBMIT
@artists_views.route("/<int:artist_id>/edit", methods=["POST"])
def edit_artist_submission(artist_id):
    form = ArtistForm(request.form)
    errors = None

    if form.validate():
        try:
            artist = Artist.query.get_or_404(artist_id)
            form.populate_obj(artist)
            db.session.add(artist)
            db.session.commit()
            flash(f"Artist {artist.name} was successfully updated!")
        except IntegrityError as exec:
            logger.error(exec)
            db.session.rollback()
            errors = True
        finally:
            db.session.close()

    if form.errors or errors:
        if form.errors:
            flash_error(parse_errors(form.errors))
        else:
            artist_name = request.form.get("name", "")
        flash_error(f"An error occurred. Artist {artist_name} could not be listed")
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

    if form.validate():
        try:
            # create City object
            city_name, state = form.city._fields["name"].data, form.city.state.data
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

            artist = Artist(
                name=name,
                genres=genres,
                city=city,
                contact_info=contact_info,
            )
            db.session.add(artist)
            db.session.commit()

            flash(f"Artist {name} was successfully listed!")
        except IntegrityError as exec:
            logger.error(exec)
            db.session.rollback()
            errors = True
        finally:
            db.session.close()

    if form.errors or errors:
        if form.errors:
            flash_error(parse_errors(form.errors))
        else:
            artist_name = request.form.get("name", "")
        flash_error(f"An error occurred. Artist {artist_name} could not be listed")
        return render_template("forms/edit_artist.html", form=form)
    return redirect(url_for("index"))
