from app import app
from flask_migrate import MigrateCommand
from flask_script import Manager

if __name__ == "__main__":
    manager = Manager(app)
    manager.add_command("db", MigrateCommand)
    manager.run()
