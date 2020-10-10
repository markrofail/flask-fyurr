from flask import Blueprint, flash, redirect, render_template, request, url_for

from src.forms import ArtistForm
from src.models.artists import Artist

artists_views = Blueprint("artists", __name__)


# READ ----------------------------------------------------
# List
@artists_views.route("/", methods=["GET"])
def artists_list():
    artists = Artist.query.order_by("id").all()
    return render_template("pages/artists.html", artists=artists)


# Details
@artists_views.route("/<int:artist_id>")
def artists_detail(artist_id):
    artist = Artist.query.get(artist_id)
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
    artist = Artist.query.get(artist_id)
    return render_template("forms/edit_artist.html", form=ArtistForm(), artist=artist)


# Form SUBMIT
@artists_views.route("/<int:artist_id>/edit", methods=["POST"])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    artist = Artist.query.get(artist_id)
    return redirect(url_for("artists.show_artist", artist_id=artist))


#  CREATE -------------------------------------------------
# Form GET
@artists_views.route("/create", methods=["GET"])
def create_artist_form():
    return render_template("forms/new_artist.html", form=ArtistForm())


# Form SUBMIT
@artists_views.route("/create", methods=["POST"])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    # on successful db insert, flash success
    flash(f"Artist {request.form['name']} was successfully listed!")
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template("pages/home.html")
