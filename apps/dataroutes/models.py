
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.orm import relationship
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin

from apps import db #login_manager

from flask_sqlalchemy import SQLAlchemy

class Datastacks(db.Model):
    __tablename__ = 'Datastacks'  # Updated to match correct table name
    id                = db.Column(db.Integer, primary_key=True)
    datastack_name    = db.Column(db.String(128), nullable=False)  # 'name' from API
    api_url           = db.Column(db.String(256), nullable=True)
    basic_info        = db.Column(db.Text, nullable=True)
    detailed_info     = db.Column(db.Text, nullable=True)
    provider          = db.Column(db.String(128), nullable=True)
    thumbnail         = db.Column(db.String(256), nullable=True)
    url               = db.Column(db.String(256), nullable=True)
    metadata_url      = db.Column(db.String(256), nullable=True)
    version           = db.Column(db.String(64), nullable=True)
    date_published    = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_updated      = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    sample_data_url   = db.Column(db.String(256), nullable=True)
    license_url       = db.Column(db.String(256), nullable=True)
    cost_of_service   = db.Column(db.String(255), default='0', nullable=True)
    # JSON fields (store as text, convert in Python)
    keywords           = db.Column(db.Text, nullable=True)  # Store as JSON string
    data_fields        = db.Column(db.Text, nullable=True)  # Store as JSON string
    subscription_model = db.Column(db.Text, nullable=True)  # Store as JSON string
    approval_based_model = db.Column(db.Text, nullable=True)
    

    def to_dict(self):
        """Convert model instance to dictionary for API response"""
        return {
            "id": self.id,
            "name": self.datastack_name,
            "api_url": self.api_url,
            "basic_info": self.basic_info,
            "detailed_info": self.detailed_info,
            "provider": self.provider,
            "thumbnail": self.thumbnail,
            "metadata_url": self.metadata_url,
            "version": self.version,
            "date_published": self.date_published,
            "last_updated": self.last_updated,
            "keywords": self.get_keywords(),
            "data_fields_present": self.get_data_fields(),
            "subscription_model": self.subscription_model,
            "approval_based_model": self.approval_based_model,
            "sample_data_url": self.sample_data_url,
            "license_url": self.license_url,
            "cost_of_service": self.cost_of_service

    }

    def get_keywords(self):
        """Convert JSON string to list"""
        return self.keywords.split(",") if self.keywords else []

    def get_data_fields(self):
        """Convert JSON string to list"""
        return self.data_fields.split(",") if self.data_fields else []
        
        
class SubscriptionRequests(db.Model):
    __tablename__ = 'SubscriptionRequests'
    request_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    data_requested_id =  db.Column(db.Integer, db.ForeignKey('Datastacks.id') , nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    status_of_request = db.Column(db.Enum('pending', 'accepted', 'rejected', name='request_status'), default='pending', nullable=False)
    remarks = db.Column(db.Text, nullable=True)
    approver_rejector_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=True)
    user = db.relationship('Users', foreign_keys=[user_id], backref='requests_made')
    approver_rejector = db.relationship('Users', foreign_keys=[approver_rejector_id], backref='requests_reviewed')
    datastack = db.relationship('Datastacks', foreign_keys=[data_requested_id], backref='datastacks_requests')
    document_proof = db.Column(db.String(255), nullable=True)  # Store file path
    identity_proof = db.Column(db.String(255), nullable=True)  # Store file path
    
    
    status_of_request_if_subscription_model_is_paid = db.Column(db.Enum('pending', 'unpaid', 'paid', '', name='request_status_if_paid_model'), default='', nullable=False)
    cost_of_request_if_subscription_model_is_paid = db.Column(db.String(255), default='0')
    transaction_details_of_request_if_subscription_model_is_paid = db.Column(db.String(255), default='')


    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            setattr(self, property, value)


    def __repr__(self):
        return f"<Request {self.request_id} by User {self.user_id} - Status: {self.status_of_request}>"


# @login_manager.user_loader
# def user_loader(id):
#     return Users.query.filter_by(id=id).first()


# @login_manager.request_loader
# def request_loader(request):
#     username = request.form.get('username')
#     user = Users.query.filter_by(username=username).first()
#     return user if user else None
