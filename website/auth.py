from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from bson import ObjectId

auth = Blueprint('auth',__name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        securityKey = request.form.get('security')

        user = User.find_by_email(email)
        
        if user:
            if check_password_hash(user['password'], password) == False:
                flash("Incorrect password", category='error')

            elif user['security_key'] != securityKey:
                flash("Incorrect security key", category='error')

            elif user and check_password_hash(user['password'], password):
                user = User(user['_id'], user['email'], user['password'], user['first_name'], user['last_name'], user['age'], user['address'], user['security_key'])
                # Log in the user
                login_user(user, remember=True)
                flash('Logged in successfully!', category='success')
                return redirect(url_for('views.home'))
            
        else:
            flash('User not found. Please sign up', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        first_name = request.form.get('firstName')
        last_name = ""
        age = ""
        address = ""
        securityKey = request.form.get('security')
        
        existing_user = User.find_by_email(email)

        if existing_user:
            flash('Email already exists. Log in instead.', category='error')
        else:

            new_user = User(ObjectId(), email, generate_password_hash(password, method='sha256'), first_name, last_name, age, address, securityKey)
            new_user.save()  # Save the new user to MongoDB
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/renew', methods=['GET', 'POST'])
def renew():
    if request.method == 'POST':
        email = request.form.get('email')
        newPassword1 = request.form.get('newPassword')
        newPassword2 = request.form.get('newPassword2')
        securityKey = request.form.get('security')

        user = User.find_by_email(email)
        if user:
            if(securityKey!=user["security_key"]):
                flash("Incorrect security key", category='error')

            elif newPassword1 == newPassword2:
                newPassword = generate_password_hash(newPassword1, method='sha256')
                User.update_password(user['_id'], newPassword)
                flash("Password updated successfully", category='success')
                return redirect(url_for('auth.login'))
            
            else:
                flash("The passwords don't match", category='error')

        else:
            flash("Cannot find user", category='error')

    return render_template('renew.html', user=current_user)