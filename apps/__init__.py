

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from datetime import datetime
import os

db = SQLAlchemy()
login_manager = LoginManager()


from apps.authentication.models import Users  # Import Users model
from apps.dataroutes.models import Datastacks
# from apps.authentication.util import hash_pass

import requests
from flask import current_app



def new_admin():
    default_users = [
        { "register":"Yes",
            "first_name": "Muneeb",
            "last_name": "Ahmed",
            "date_of_birth": datetime.strptime("09/04/1995", "%m/%d/%Y").date(),
            "username": "muneeb",
            "email": "muneebpandith@gmail.com",
            "phone": "9149429559",
            "password": "Y@y686332",  # API will hash it
            "role": 1,  # Admin user
            "type_of_organization": "Government",
            "name_of_organization": "Skill Development Department",
            "country": "India",
            "address": "Srinagar",
            "state": "J&K",
            "city_town": "Srinagar",
            "pincode": "190018",
            "oauth_github": None
            }
        ]
    if Users.query.first():
        print({"error": "Admin registration is disabled, as admin already exists."}), 403
    else:
        user = Users(**default_users[0])
        db.session.add(user)
        db.session.commit()
        # Delete user from session
        logout_user()


def new_datastack():
    DATASTACK_AVAILABLE = [{
        'id':1,
        'datastack_name': 'Household and Heads of households',
        'thumbnail':'/static/assets/images/households.jpg',
        'basic_info': 'This dataset includes information on households, including household size, composition, and the head of household details.',
        'detailed_info': 'The dataset provides demographic and economic characteristics of households, including income levels, dwelling types, and family structures. Useful for social research and policy formulation.',
        'keywords': "household,family,demographics,income,housing",
        'version': '1.0',
        'data_fields': "household_id,head_name,household_size,income_bracket,dwelling_type",
        'date_published': datetime.strptime("02/25/2025", "%m/%d/%Y").date(),
        'last_updated': datetime.strptime("02/25/2025", "%m/%d/%Y").date(),
        'provider': 'Mission YUVA',
        'url': 'SECRET URL 1',
        'metadata_url':'',
        'api_url':'api/v1/data/1',
        'subscription_model':'Free',
        'approval_based_model':'yes',

    },
    {
        'id':2,
        'datastack_name': 'Individual Members',
        'thumbnail':'/static/assets/images/individual_members.avif',
        'basic_info': 'Contains demographic and personal data for individual members of households.',
        'detailed_info': 'Includes age, gender, education level, employment status, and relationship to the household head. Helps in analyzing population structures.',
        'keywords': "individual,demographics,education,employment",
        'version': '1.0',
        'data_fields': "member_id,name,age,gender,education,employment_status",
        'date_published': datetime.strptime("02/25/2025", "%m/%d/%Y").date(),
        'last_updated': datetime.strptime("02/25/2025", "%m/%d/%Y").date(),
        'provider': 'Mission YUVA',
        'url': 'SECRET URL 2',
        'metadata_url':'',
        'api_url':'api/v1/data/2',
        'subscription_model':'Free',
        'approval_based_model':'yes',
    },
    {
        'id':3,
        'datastack_name': 'Potential Entrepreneurs (Unregistered Activities)',
        'thumbnail':'/static/assets/images/PEUR.webp',
        'basic_info': 'Focuses on individuals engaged in informal, unregistered economic activities.',
        'detailed_info': 'Provides insights into the informal sector, covering types of activities, income generation, and barriers to registration.',
        'keywords': "entrepreneurship,informal sector,small business,self-employment",
        'version': '1.0',
        'data_fields': "entrepreneur_id,activity_type,income_level,business_duration",
        'date_published': datetime.strptime("02/25/2025", "%m/%d/%Y").date(),
        'last_updated': datetime.strptime("02/25/2025", "%m/%d/%Y").date(),
        'provider': 'Mission YUVA',
        'url': 'SECRET URL 3',
        'metadata_url':'',
        'api_url':'api/v1/data/3',
        'subscription_model':'Free',
        'approval_based_model':'yes',
    },
    {
        'id':4,
        'datastack_name': 'Potential Entrepreneurs (Unemployed)',
        'thumbnail':'/static/assets/images/PEU.webp',
        'basic_info': 'Covers unemployed individuals considering entrepreneurship as a livelihood option.',
        'detailed_info': 'Includes information on skills, previous employment, business interests, and challenges faced in starting a business.',
        'keywords': "unemployment,business,entrepreneurship,skills development",
        'version': '1.0',
        'data_fields': "individual_id,previous_job,skills,business_interest,challenges",
        'date_published': datetime.strptime("02/25/2025", "%m/%d/%Y").date(),
        'last_updated': datetime.strptime("02/25/2025", "%m/%d/%Y").date(),
        'provider': 'Mission YUVA',
        'url': 'SECRET URL 4',
        'metadata_url':'',
        'api_url':'api/v1/data/4',
        'subscription_model':'Free',
        'approval_based_model':'yes',
    },
    {
        'id':5,
        'datastack_name': 'Potential Entrepreneurs (Employed)',
        'thumbnail':'/static/assets/images/PEE.webp',
        'basic_info': 'Examines employed individuals looking to transition into entrepreneurship.',
        'detailed_info': 'Includes job roles, industries, savings, and motivation for starting a business, aiding in business support planning.',
        'keywords': "entrepreneurship,career change,business planning",
        'version': '1.0',
        'data_fields': "employee_id,current_job,industry,savings,business_motivation",
        'date_published': datetime.strptime("02/25/2025", "%m/%d/%Y").date(),
        'last_updated': datetime.strptime("02/25/2025", "%m/%d/%Y").date(),
        'provider': 'Mission YUVA',
        'url': 'SECRET URL 5',
        'metadata_url':'',
        'api_url':'api/v1/data/5',
        'subscription_model':'Free',
        'approval_based_model':'yes',
    }
    ]
    
    datastacks = Datastacks.query.all()
    datastacks_len = len([ds.to_dict().keys() for ds in datastacks])
    print('Available ds', datastacks_len)
    if datastacks_len >= 5 :
        print({"error": "Data Stacks creation is disabled, as basic Datastacks already exist."}), 403
    else:
        for d in DATASTACK_AVAILABLE:
            #print('Creating', d)
            d_ = Datastacks(**d)
            db.session.add(d_)
            db.session.commit()

        # Delete user from session




def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app):
    for module_name in ('authentication', 'home', 'dataroutes'):
        module = import_module('apps.{}.routes'.format(module_name))
        print("Registered "+str(module.blueprint))
        app.register_blueprint(module.blueprint)


def configure_database(app):
    @app.before_first_request
    def initialize_database():
        try:
            db.create_all()
            new_admin()
            new_datastack()
        except Exception as e:

            print('> Error: DBMS Exception: ' + str(e) )

            # fallback to SQLite
            basedir = os.path.abspath(os.path.dirname(__file__))
            app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')

            print('> Fallback to SQLite ')
            db.create_all()
            new_admin()
            new_datastack()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

from apps.authentication.oauth import github_blueprint

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)

    #app.register_blueprint(github_blueprint, url_prefix="/login")
    
    register_blueprints(app)
    configure_database(app)
    return app
