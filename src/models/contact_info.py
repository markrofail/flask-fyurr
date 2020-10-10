from src.models import db


class ContactInfo(db.Model):
    __tablename__ = "contact_info"

    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String, nullable=False)
    image_link = db.Column(db.String, nullable=False)
    website = db.Column(db.String, nullable=True)
    facebook_link = db.Column(db.String, nullable=True)