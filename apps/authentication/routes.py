
import re
from flask import render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user
)
from datetime import datetime
from flask_dance.contrib.github import github
from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm
from apps.authentication.models import Users
from apps.authentication.util import verify_pass

# @blueprint.route('/')
# def route_default():
#     return redirect(url_for('authentication_blueprint.login'))


@blueprint.route('/')
def route_default():
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = Users.query.filter_by(username=username).first()

        # Check the password
        if user and verify_pass(password, user.password):
            login_user(user)
            return redirect(url_for('authentication_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Wrong user or password',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)
    return redirect(url_for('home_blueprint.index'))


def validate_fields(request_form):
    errors = []
    first_name = request_form['first_name']
    last_name = request_form['last_name']
    date_of_birth = request_form['date_of_birth']
    type_of_organization = request_form['type_of_organization']
    name_of_organization = request_form['name_of_organization']
    country = request_form['country']
    address = request_form['address']
    city_town = request_form['city_town']
    pincode = request_form['pincode']
    email = request_form['email']
    username= request_form['username']
    state= request_form['state']
    
    phone = request_form['phone']
    password = request_form['password']
    
    # Validate First Name (Required, only letters and spaces, max 64 chars)
    if not re.fullmatch(r"^[A-Za-z\s]+$", first_name) or len(first_name) > 64:
        errors.append("First name must contain only letters and spaces, and be less than 64 characters.")

    # Validate Last Name (Required, only letters and spaces, max 64 chars)
    if not re.fullmatch(r"^[A-Za-z\s]+$", last_name) or len(last_name) > 64:
        errors.append("Last name must contain only letters and spaces, and be less than 64 characters.")

    # Validate Date of Birth (Must be a valid date and user should be at least 18)
    try:
        dob = datetime.strptime(date_of_birth, "%m/%d/%Y").date()
        age = (datetime.today().date() - dob).days // 365
        if age < 18:
            errors.append("You must be at least 18 years old to register.")
    except ValueError:
        errors.append("Invalid date format for Date of Birth.")

    # # Validate Country (Required, only letters, max 64 chars)
    # if not re.fullmatch(r"^[A-Za-z\s]+$", country) or len(country) > 64:
    #     errors.append("Country must contain only letters and spaces, and be less than 64 characters.")

    # Validate Address (Required, at least 10 characters)
    if not re.search(r"[A-Za-z]", address) or not re.fullmatch(r"^[A-Za-z0-9\s\W]+$", address):
        errors.append("Address must contain at least one letter and can include letters, numbers, spaces, and/or special characters.")

    # Validate City/Town (Required, only letters and spaces, max 64 chars)
    if not re.fullmatch(r"^[A-Za-z\s\d]+$", city_town) or len(city_town) > 64:
        errors.append("City/Town must contain only letters, digits, spaces, and be less than 64 characters.")

    # Validate Pincode (Required, only digits, 5-10 characters)
    if not re.fullmatch(r"^\d{6,7}$", pincode):
        errors.append("Pincode must be a number between 6 or 7 digits long.")

    # Validate Email (Required, proper email format)
    if not re.fullmatch(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
        errors.append("Invalid email format.")

    # Validate Phone Number (Required, 10-15 digits)
    if not re.fullmatch(r"^\d{10,11}$", phone):
        errors.append("Phone number must be 10-digits or 11-digits long.")

    if not re.fullmatch(r"^[A-Za-z0-9]{6,}$", username):
        errors.append("Username must be at least 6 characters long and contain only letters and digits. No symbols or spaces allowed.")
    
    if not re.search(r"[A-Za-z]", name_of_organization) or not re.fullmatch(r"^[A-Za-z0-9\s\W]+$", name_of_organization):
        errors.append("Organization name must contain at least one letter and can include letters, numbers, spaces, and/or special characters.")

    if not country == "India":
        errors.append("Country must be India.")
    
    if not state == "J&K":
        errors.append("State must be J&K.")
        
    if not type_of_organization in ["Government", "Individual", "R&D", "Academic Institutes"]:
        errors.append("Type of organization can be: Government, R&D, Academic Institutes or Individuals.")

    if not re.fullmatch(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", password):
        errors.append("Password must be at least 8 characters long and include one uppercase letter, one lowercase letter, one number, and one special character.")

    err = ""
    
    if errors:
        err = "<ul style='background-color:#ffae9c73; padding:40px; border-radius:2px; border: 1px solid #fc6262;'>"
        for e in errors:
            err += "<li style='color:red';>"+str(e)+"</li>"
        err += "</ul>"
    return err


#ImmutableMultiDict([('csrf_token', 'IjQzYTdiM2VhMWE3MzZlZDUyZGEzYWU1MzcwMWYyMzRjYTJhMjU3ZTIi.Z7MPKQ.ecA-R6WWrJqVy4fOLmAWxvNcX-w'), 
# ('first_name', 'Hello'), ('last_name', 'Hello'), 
# ('date_of_birth', '02/17/2025'), 
# ('type_of_organization', 'Academic Institutes'), 
# ('name_of_organization', 's'), 
# ('country', 'India'), 
# ('address', 'wsw'), ('state', '1'), 
# ('city_town', 'wsws'), 
# ('pincode', 'wswsws'), 
# ('email', 'wswswsws@gmail.coim'), 
# ('phone', '9149429559'), ('username', '12muneeb12'), 
# ('password', 'Hello@123456'), 
# ('register', '')])








@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']

        

        # Check usename exists
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)

        errors = validate_fields(request.form)

        if errors:
            return render_template('accounts/register.html',
                                   msg=errors,
                                   success=False,
                                   form=create_account_form)




        request_form_cleaned = request.form.copy()
        if isinstance(request_form_cleaned['date_of_birth'], str):
            request_form_cleaned['date_of_birth'] = datetime.strptime(request_form_cleaned['date_of_birth'], "%m/%d/%Y").date()


        # else we can create the user
        user = Users(**request_form_cleaned)
        
        # user = Users(
        #     first_name=create_account_form.first_name.data,
        #     last_name=create_account_form.last_name.data,
        #     date_of_birth=create_account_form.date_of_birth.data,
        #     username=username,
        #     email=email,
        #     password=hash_pass(create_account_form.password.data),  # Hashing password
        #     type_of_organization=create_account_form.type_of_organization.data,
        #     name_of_organization=create_account_form.name_of_organization.data,
        #     country=create_account_form.country.data,
        #     address=create_account_form.address.data,
        #     state=create_account_form.state.data,
        #     city_town=create_account_form.city_town.data,
        #     pincode=create_account_form.pincode.data,
        #     role=0  # Default user role
        # )


        db.session.add(user)
        db.session.commit()

        # Delete user from session
        logout_user()
        
        return render_template('accounts/register.html',
                               msg='Account created successfully. Login to continue.',
                               success=True,
                               form=create_account_form)

    else:
        return render_template('accounts/register.html', form=create_account_form)



@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home_blueprint.index'))


# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500
