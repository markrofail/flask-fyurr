from fyuur.models import PkModelMixin, db


class ContactInfo(PkModelMixin, db.Model):
    __tablename__ = "contact_info"

    phone = db.Column(db.String, nullable=False)
    image_link = db.Column(db.String, nullable=False)
    website = db.Column(db.String, nullable=True)
    facebook_link = db.Column(db.String, nullable=True)
