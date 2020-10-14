from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class PkModelMixin:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
