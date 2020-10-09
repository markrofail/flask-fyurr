import logging

from flask_fixtures import load_fixtures_from_file
from flask_migrate import MigrateCommand
from flask_script import Manager
from sqlalchemy.exc import IntegrityError

from app import create_app
from src.models import db

logger = logging.getLogger(__name__)

manager = Manager(create_app)


@manager.command
def seed():
    fixtures = ["artists.json", "venues.json", "shows.json"]
    for fixture in fixtures:
        try:
            load_fixtures_from_file(db=db, fixture_filename=f"src/fixtures/{fixture}")
        except IntegrityError as e:
            logger.error(e)


manager.add_command("db", MigrateCommand)
manager.run()
