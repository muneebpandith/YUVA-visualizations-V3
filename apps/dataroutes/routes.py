from apps.dataroutes import blueprint
from jinja2 import TemplateNotFound
from collections import Counter
import random
import itertools
import re
from flask import render_template, redirect, request, request, jsonify, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user
)
from datetime import datetime, timedelta
# from flask_dance.contrib.github import github
from apps import db, login_manager
from apps.authentication.models import Users
from apps.dataroutes.models import Datastacks, SubscriptionRequests
from apps.dataroutes.forms import CreateSubscriptionRequestForm
from flask_login import login_required, current_user
from apps.authentication.util import verify_pass
from apps.dataroutes.util import Uploader
import time
from werkzeug.utils import secure_filename
import hashlib
from sqlalchemy import desc


#import magic #for checking mime type in python



u = Uploader()






# def prepare_datastack():
#     # Should come from DB in future
#     DATASTACK_AVAILABLE = dict()
#     DATASTACK_AVAILABLE['household'] = {
#         'name': 'Household and Heads of households',
#         'thumbnail':'/static/assets/images/households.jpg',
#         'basic_info': 'This dataset includes information on households, including household size, composition, and the head of household details.',
#         'detailed_info': 'The dataset provides demographic and economic characteristics of households, including income levels, dwelling types, and family structures. Useful for social research and policy formulation.',
#         'keywords': ['household', 'family', 'demographics', 'income', 'housing'],
#         'version': '1.0',
#         'data_fields_present': ['household_id', 'head_name', 'household_size', 'income_bracket', 'dwelling_type'],
#         'date_published': '2024-02-01',
#         'last_updated': '2024-02-01',
#         'provider': 'Mission YUVA',
#         'url': '/data/household',
#         'api_url':'api/v1/data/household',
#         'subscription_model':'Free, Approval-Based'

#     }

#     DATASTACK_AVAILABLE['individual_members'] = {
#         'name': 'Individual Members',
#         'thumbnail':'/static/assets/images/individual_members.avif',
#         'basic_info': 'Contains demographic and personal data for individual members of households.',
#         'detailed_info': 'Includes age, gender, education level, employment status, and relationship to the household head. Helps in analyzing population structures.',
#         'keywords': ['individual', 'demographics', 'education', 'employment'],
#         'version': '1.0',
#         'data_fields_present': ['member_id', 'name', 'age', 'gender', 'education', 'employment_status'],
#         'date_published': '2024-02-01',
#         'last_updated': '2024-02-01',
#         'provider': 'Mission YUVA',
#         'url': '/data/individual_members',
#         'api_url':'api/v1/data/individual_members',
#         'subscription_model':'Free, Approval-Based'
#     }

#     DATASTACK_AVAILABLE['peur'] = {
#         'name': 'Potential Entrepreneurs (Unregistered Activities)',
#         'thumbnail':'/static/assets/images/PEUR.webp',
#         'basic_info': 'Focuses on individuals engaged in informal, unregistered economic activities.',
#         'detailed_info': 'Provides insights into the informal sector, covering types of activities, income generation, and barriers to registration.',
#         'keywords': ['entrepreneurship', 'informal sector', 'small business', 'self-employment'],
#         'version': '1.0',
#         'data_fields_present': ['entrepreneur_id', 'activity_type', 'income_level', 'business_duration'],
#         'date_published': '2024-02-01',
#         'last_updated': '2024-02-01',
#         'provider': 'Mission YUVA',
#         'url': '/data/peur',
#         'api_url':'api/v1/data/peur',
#         'subscription_model':'Free, Approval-Based'
#     }

#     DATASTACK_AVAILABLE['peu'] = {
#         'name': 'Potential Entrepreneurs (Unemployed)',
#         'thumbnail':'/static/assets/images/PEU.webp',
#         'basic_info': 'Covers unemployed individuals considering entrepreneurship as a livelihood option.',
#         'detailed_info': 'Includes information on skills, previous employment, business interests, and challenges faced in starting a business.',
#         'keywords': ['unemployment', 'business', 'entrepreneurship', 'skills development'],
#         'version': '1.0',
#         'data_fields_present': ['individual_id', 'previous_job', 'skills', 'business_interest', 'challenges'],
#         'date_published': '2024-02-01',
#         'last_updated': '2024-02-01',
#         'provider': 'Mission YUVA',
#         'url': '/data/peu',
#         'api_url':'api/v1/data/peu',
#         'subscription_model':'Free, Approval-Based'
#     }

#     DATASTACK_AVAILABLE['pee'] = {
#         'name': 'Potential Entrepreneurs (Employed)',
#         'thumbnail':'/static/assets/images/PEE.webp',
#         'basic_info': 'Examines employed individuals looking to transition into entrepreneurship.',
#         'detailed_info': 'Includes job roles, industries, savings, and motivation for starting a business, aiding in business support planning.',
#         'keywords': ['entrepreneurship', 'career change', 'business planning'],
#         'version': '1.0',
#         'data_fields_present': ['employee_id', 'current_job', 'industry', 'savings', 'business_motivation'],
#         'date_published': '2024-02-01',
#         'last_updated': '2024-02-01',
#         'provider': 'Mission YUVA',
#         'url': '/data/pee',
#         'api_url':'api/v1/data/pee',
#         'subscription_model':'Free, Approval-Based'
#     }
#     return DATASTACK_AVAILABLE


@blueprint.route('/api/v1/')
def get_home_api(): 
    return jsonify({"message":"You have reached the end-point of API v1 of YUVA Datastack."})



@blueprint.route('/api/v1/data/')
def get_datastack(): 
    datastacks = Datastacks.query.all()
    datastacks_available = [ds.to_dict()for ds in datastacks]
    return jsonify({"datastack":datastacks_available})


@blueprint.route('/api/v1/data/<key>/')
def get_api_data_detailed(key):
    try:
        #print('KEYYY',key)
        key = int(key)  # Ensure key is an integer
        #print('KEYYY',key)
        if key is None:
            return jsonify({"error": "Invalid ID"}), 400  # Return Bad Request
        
        datastack = Datastacks.query.filter_by(id=key).first()
        
        if not datastack:
            return jsonify({"error": "Datastack not found"}), 404  # Return Not Found
        # Convert SQLAlchemy object to dictionary
        return jsonify({
            "datastack": {
                "id": datastack.id,
                "name": datastack.datastack_name,
                "api_url": datastack.api_url,
                "basic_info": datastack.basic_info,
                "detailed_info": datastack.detailed_info,
                "keywords": str(datastack.keywords).replace("{","").replace("}","").replace("'","").replace(" ","").split(","),  # Assuming stored as CSV
                "version": datastack.version,
                "provider": datastack.provider,
                "date_published": datastack.date_published,
                "last_updated": datastack.last_updated,
                "thumbnail": datastack.thumbnail,
                "metadata_url": datastack.metadata_url,
                "subscription_model":datastack.subscription_model,
                "approval_based_model":datastack.approval_based_model,
                "sample_data_url":datastack.sample_data_url,
                "license_url":datastack.license_url,
                "cost_of_service":datastack.cost_of_service

            }
        })
    except Exception as e:
        return jsonify({"error": "An error occurred"}), 500  # Return Internal Server Error


    

@blueprint.route('/data/')
def data():
    try:
        if(current_user.id):
            return render_template('home/data.html', segment='data', user_id=current_user.id, user_role = current_user.role)
    except Exception as e:
        #print('Did exceptions')
        return render_template('home/data.html', segment='data', user_id="", user_role = "")



@blueprint.route('/dashboard/')
@login_required
def dashboard():

    #check for role
    if current_user.is_admin():
        #db acccesses needed to admin
        pass
    else:
        #db accesses needed to user
        pass
    
    existing_requests_requests_joinedwith_datastacks = (
        db.session.query(SubscriptionRequests, Datastacks)
        .join(Datastacks, SubscriptionRequests.data_requested_id == Datastacks.id)
        .filter(SubscriptionRequests.user_id == current_user.id)
        .order_by(desc(SubscriptionRequests.creation_date))
        .all()
    )
    #print(existing_requests_requests_joinedwith_datastacks)
   
    #existing_requests = SubscriptionRequests.query.filter_by(user_id=current_user.id).all()

    #requests_with_users = db.session.query(SubscriptionRequest, User).join(User).all()

    try:
        if(current_user.id):
            return render_template('home/dashboard.html', segment='dashboard', user_id=current_user.id, user_role = current_user.role, existing_requests= existing_requests_requests_joinedwith_datastacks)
    except Exception as e:
        #print('Did exceptions')
        return render_template('home/dashboard.html', segment='dashboard', user_id="", user_role = "", existing_requests= "")




@blueprint.route('/data/<key>/')
def get_data_detailed(key):
    try:
        #print('KEYYY',key)
        key = int(key)  # Ensure key is an integer
        if key is None:
            return render_template('home/page-404.html'), 404
        datastack = Datastacks.query.filter_by(id=key).first()
        
        if not datastack:
            return render_template('home/page-404.html'), 404

        ds = {
                "id": datastack.id,
                "name": datastack.datastack_name,
                "api_url": datastack.api_url,
                "basic_info": datastack.basic_info,
                "detailed_info": datastack.detailed_info,
                "keywords": str(datastack.keywords).replace("{","").replace("}","").replace("'","").split(","),  # Assuming stored as CSV
                "data_fields": str(datastack.data_fields).replace("{","").replace("}","").replace("'","").split(","),  # Assuming stored as CSV
                "version": datastack.version,
                "provider": datastack.provider,
                "date_published": datastack.date_published,
                "last_updated": datastack.last_updated,
                "thumbnail": datastack.thumbnail,
                "metadata_url": datastack.metadata_url,
                "subscription_model":datastack.subscription_model,
                "approval_based_model":datastack.approval_based_model,
                "sample_data_url":datastack.sample_data_url,
                "license_url":datastack.license_url,
                "cost_of_service":datastack.cost_of_service

        }


        
        #ds = datastack.copy()
        #ds["keywords"] = str(ds.keywords).replace("{","").replace("}","").replace("'","").replace(" ","").split(",")
        try:
            if(current_user.id):
                return render_template('home/data_detailed.html', segment='data', data=ds, user_id=current_user.id, user_role = current_user.role)
        except Exception as e:
            return render_template('home/data_detailed.html',segment='data', data=ds, user_id = "", user_role="")
    except Exception as e:
        return render_template('home/page-404.html'), 404




@blueprint.route('/request-datastack/', methods=['GET', 'POST'])
def get_default_route_request_datastack():
    return render_template('home/page-404.html'), 404

#mime = magic.Magic(mime=True) # for checking MIME types



def validate_upload_fields( authority_doc_data, identity_doc_data ,purpose):
    errors = []

    if not authority_doc_data:
        errors.append("Authority document is necessary.")
    
    if authority_doc_data:
        if not u.file_type_valid(authority_doc_data, validated_filetypes=["application/pdf"]):
            errors.append("Kindly upload a valid authority document (Only PDF format is allowed).")
        
        if not u.file_size_valid(authority_doc_data):
            errors.append("Kindly upload a valid authority document (Maximum allowed filesize is 500 Kb).")
    
    if identity_doc_data:
        if not u.file_type_valid(identity_doc_data, validated_filetypes=["application/pdf"]):
            errors.append("Kindly upload a valid identity document (Only PDF format is allowed).")
        
        if not u.file_size_valid(identity_doc_data):
            errors.append("Kindly upload a valid identity document (Maximum allowed filesize is 500 Kb).")



    if not purpose:
        errors.append("Adding details of pupose of requesting datatack is required.")

    err = ""
    if errors:
        err = "<ul style='background-color:#ffae9c73; padding:40px; border-radius:2px; border: 1px solid #fc6262;'>"
        for e in errors:
            err += "<li style='color:red';>"+str(e)+"</li>"
        err += "</ul>"
    return err


@blueprint.route('/request-datastack/<key>/', methods=['GET', 'POST'])
@login_required
def request_datastack(key):
    create_request_form = CreateSubscriptionRequestForm(request.form)
    try:
        key = int(key)  # Ensure key is an integer
        if key is None:
            return render_template('home/page-404.html'), 404
        datastack = Datastacks.query.filter_by(id=key).first()
        if not datastack:
            return render_template('home/page-404.html'), 404
    except Exception as e:
        return render_template('home/page-404.html'), 404


    if 'request-datastack' in request.form:
        # if not datastack handled earlier
        # if datastack:
        #     errors = None #validate_subscription_form(request.form)
        #     if errors:
        #         return render_template('home/request-datastack.html',
        #                                msg=errors,
        #                                success=False,
        #                                form=create_request_form, datastack=datastack)

        
        authority_doc_data = request.files.get('authority_document')
        identity_doc_data = request.files.get('identity_document')
        purpose = request.form['purpose']

        errors = validate_upload_fields( authority_doc_data,identity_doc_data,purpose)
        if errors:
            return render_template('home/request-datastack.html',
                                   msg=errors,
                                   success=False,
                                   form=create_request_form, datastack=datastack)






        
        
        #request_form_cleaned['status_of_request_if_subscription_model_is_paid']=''
        #request_form_cleaned['transaction_details_of_request_if_subscription_model_is_paid']=''
        #request_form_cleaned['approver_rejector_id'] = 999
        
        last_24_hours = datetime.utcnow() - timedelta(hours=24)
        existing_request = SubscriptionRequests.query.filter_by(data_requested_id=datastack.id, user_id=current_user.id, status_of_request='pending').first()
        

        #print(last_24_hours, existing_request.creation_date)
        if existing_request and existing_request.creation_date > last_24_hours:
            return render_template('home/request-datastack.html',
                                   msg="<b> You have already made a request for this datastack which is under process. Kindly wait at least 24 hours to make a new request for the same datastack.",
                                   success=True,
                                   form=create_request_form, datastack=datastack)

        
        request_form_cleaned = request.form.copy()
        request_form_cleaned['user_id'] = current_user.id
        request_form_cleaned['data_requested_id'] = datastack.id
        request_form_cleaned['creation_date'] = datetime.utcnow()
        request_form_cleaned['updated_date'] = None
        request_form_cleaned['status_of_request'] = 'pending'
        request_form_cleaned['remarks'] = ''


        if not datastack.approval_based_model == "yes":
            request_form_cleaned['status_of_request'] = 'accepted'
            request_form_cleaned['updated_date'] = datetime.utcnow()
            request_form_cleaned['approver_rejector_id'] = None
            request_form_cleaned['remarks'] = 'AUTO-APPROVED'

        # if not is_permissible(user_id_organization, datastack_id):
        #     request_form_cleaned['status_of_request'] = 'rejected'
        #     request_form_cleaned['updated_date'] = datetime.utcnow()
        #     request_form_cleaned['approver_rejector_id'] = None
        #     request_form_cleaned['remarks'] = 'AUTO-REJECTED AS THIS DATASTACK IS NOT AVAILABLE FOR THIS ORGANIZATION'
        
        if not datastack.subscription_model == "free":
            request_form_cleaned['status_of_request_if_subscription_model_is_paid'] = 'unpaid'
            request_form_cleaned['cost_of_request_if_subscription_model_is_paid'] = datastack.cost_of_service

        sha = hashlib.sha256()
        authority_doc_og_name = authority_doc_data.filename
        sha.update((str(time.time())+str(secure_filename(authority_doc_og_name))).encode())
        authority_doc_url_sha = sha.hexdigest()
        #print('AU HEX URL', authority_doc_url_sha)
        _, authority_doc_url = u.upload(fn = str(current_user.id)+'-'+str(datastack.id)+'-A-'+str(authority_doc_url_sha)+".pdf", df = authority_doc_data)
        
        if not _ == "0":
            return render_template('home/request-datastack.html',
                                   msg="An error occured while uploading the Authority document. Please try again",
                                   success=False,
                                   form=create_request_form,  datastack=datastack)

        
        sha = hashlib.sha256()
        identity_doc_og_name = identity_doc_data.filename
        sha.update((str(time.time())+str(secure_filename(identity_doc_og_name))).encode())
        identity_doc_url_sha = sha.hexdigest()
        #print('ID HEX URL', identity_doc_url_sha)
        _ , identity_doc_url = u.upload(fn = str(current_user.id)+'-'+str(datastack.id)+'-D-'+str(identity_doc_url_sha)+".pdf", df = identity_doc_data)
        
        if not _ == "0":
            return render_template('home/request-datastack.html',
                                   msg="An error occured while uploading the Identity document. Please try again",
                                   success=False,
                                   form=create_request_form,  datastack=datastack)
        


        request_form_cleaned['document_proof'] = authority_doc_url
        request_form_cleaned['identity_proof'] = identity_doc_url

        datastack_user_subscription = SubscriptionRequests(**request_form_cleaned)

        db.session.add(datastack_user_subscription)
        db.session.commit()        
        return render_template('home/request-datastack.html',
                               msg='Datastack request submitted successfully. Kindly follow the status of the request in Subscription tab of your Dashboard. Please wait for the approval. ',
                               success=True)

    else:
        return render_template('home/request-datastack.html', form=create_request_form, datastack=datastack)





# from flask import Flask, request, redirect, url_for, send_from_directory, flash
# from werkzeug.utils import secure_filename

# UPLOAD_FOLDER = "uploads"
# ALLOWED_EXTENSIONS = {'pdf', 'docx', 'xlsx'}

# app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route("/upload", methods=["POST"])
# def upload_file():
#     if "file" not in request.files:
#         flash("No file part")
#         return redirect(request.url)

#     file = request.files["file"]
    
#     if file.filename == "":
#         flash("No selected file")
#         return redirect(request.url)

#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
#         file.save(file_path)

#         # Save file_path to SubscriptionRequests model
#         request_id = request.form.get("request_id")  # Assume you send this in the form
#         subscription_request = SubscriptionRequests.query.get(request_id)
#         if subscription_request:
#             subscription_request.file_path = file_path
#             db.session.commit()

#         return redirect(url_for("view_requests"))
    
#     flash("Invalid file format")
#     return redirect(request.url)




@blueprint.route('/test1/')
def test1_route():
    return render_template('home/tables-bootstrap-tables.html')


@blueprint.route('/test2/')
def test2_route():
    return render_template('home/settings.html')


@blueprint.route('/test3/')
def test3_route():
    return render_template('home/transactions.html')
    
    