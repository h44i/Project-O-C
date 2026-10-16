from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


def now():
    return datetime.now(timezone.utc)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(120))
    country = db.Column(db.String(80))
    university = db.Column(db.String(120))
    language = db.Column(db.String(10), default="ru")
    role = db.Column(db.String(20), default="student")
    created_at = db.Column(db.DateTime, default=now)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Status(db.Model):
    __tablename__ = "statuses"
    __table_args__ = (db.UniqueConstraint("code", "entity"),)

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    entity = db.Column(db.String(20), nullable=False)


class Guide(db.Model):
    __tablename__ = "guides"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    category = db.Column(db.String(50))
    language = db.Column(db.String(10), default="ru")
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=now)

    author = db.relationship("User")


class Place(db.Model):
    __tablename__ = "places"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50))
    address = db.Column(db.String(255))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    phone = db.Column(db.String(30))
    hours = db.Column(db.String(100))


class Step(db.Model):
    __tablename__ = "steps"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    order_num = db.Column(db.Integer, nullable=False)
    guide_id = db.Column(db.Integer, db.ForeignKey("guides.id"))
    place_id = db.Column(db.Integer, db.ForeignKey("places.id"))
    deadline_days = db.Column(db.Integer)

    guide = db.relationship("Guide")
    place = db.relationship("Place")


class UserStep(db.Model):
    __tablename__ = "user_steps"
    __table_args__ = (db.UniqueConstraint("user_id", "step_id"),)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    step_id = db.Column(db.Integer, db.ForeignKey("steps.id"), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey("statuses.id"), nullable=False)
    updated_at = db.Column(db.DateTime, default=now, onupdate=now)

    user = db.relationship("User")
    step = db.relationship("Step")
    status = db.relationship("Status")


class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    volunteer_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    step_id = db.Column(db.Integer, db.ForeignKey("steps.id"))
    place_id = db.Column(db.Integer, db.ForeignKey("places.id"))
    status_id = db.Column(db.Integer, db.ForeignKey("statuses.id"), nullable=False)
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=now)

    student = db.relationship("User", foreign_keys=[user_id])
    volunteer = db.relationship("User", foreign_keys=[volunteer_id])
    step = db.relationship("Step")
    place = db.relationship("Place")
    status = db.relationship("Status")
