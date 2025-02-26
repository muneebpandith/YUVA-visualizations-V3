
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.orm import relationship
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin

from apps import db, login_manager

from apps.authentication.util import hash_pass



class Users(db.Model, UserMixin):
    __tablename__ = 'Users'
    id                  = db.Column(db.Integer, primary_key=True)
    first_name          = db.Column(db.String(64), nullable=False)
    last_name           = db.Column(db.String(64), nullable=False)
    date_of_birth       = db.Column(db.Date, nullable=False)
    username            = db.Column(db.String(64), unique=True, nullable=False)
    email               = db.Column(db.String(64), unique=True, nullable=False)
    phone               = db.Column(db.String(64), unique=False, nullable=False)
    password            = db.Column(db.LargeBinary, nullable=False)
    role                = db.Column(db.Integer, default=0, nullable=False)  # 0 = Regular User, 1 = Admin
    type_of_organization = db.Column(db.String(128), nullable=True)
    name_of_organization = db.Column(db.String(128), nullable=True)
    country             = db.Column(db.String(64), nullable=False)
    address             = db.Column(db.Text, nullable=False)
    state               = db.Column(db.String(64), nullable=False)
    city_town           = db.Column(db.String(64), nullable=False)
    pincode             = db.Column(db.String(20), nullable=False)
    oauth_github        = db.Column(db.String(100), nullable=True)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username) 

    def is_admin(self):
        return self.role == 1  # Helper method to check if user is an admin


# class Users(db.Model, UserMixin):
#     __tablename__ = 'Users'
#     id            = db.Column(db.Integer, primary_key=True)
#     username      = db.Column(db.String(64), unique=True)
#     email         = db.Column(db.String(64), unique=True)
#     password      = db.Column(db.LargeBinary)
#     role          = db.Column(db.Integer, default=0, nullable=False)  # 0 = Regular User, 1 = Admin
#     oauth_github  = db.Column(db.String(100), nullable=True)

#     def __init__(self, **kwargs):
#         for property, value in kwargs.items():
#             # depending on whether value is an iterable or not, we must
#             # unpack it's value (when **kwargs is request.form, some values
#             # will be a 1-element list)
#             if hasattr(value, '__iter__') and not isinstance(value, str):
#                 # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
#                 value = value[0]

#             if property == 'password':
#                 value = hash_pass(value)  # we need bytes here (not plain str)

#             setattr(self, property, value)

#     def __repr__(self):
#         return str(self.username) 


@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None

class OAuth(OAuthConsumerMixin, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("Users.id", ondelete="cascade"), nullable=False)
    user = db.relationship(Users)
