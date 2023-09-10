from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth',__name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email  = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('Email does not exist', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route('/signup', methods=['GET','POST'])
def signup():
    while True:
        if request.method == 'POST':
            email = request.form.get('email')
            firstName = request.form.get('firstName')
            password1 = request.form.get('password')
            password2 = request.form.get('password2')

            user = User.query.filter_by(email=email).first()
            if user:
                flash("Email already exists", category='error')

            elif len(email)==0:
                flash("Please enter an email", category='error')
            
            elif len(firstName)==0:
                flash("Please enter your first name", category='error')
            
            elif len(password1)==0:
                flash("Please enter a password", category='error')

            # Password must be at least 8 characters long
            elif len(password1) < 8:
                flash("Password must have at least 8 characters long", category='error')
        
            # Password must contain at least one uppercase letter
            elif not any(char.isupper() for char in password1):
                flash("Password must contain at least one uppercase letter", category='error')
        
            # Password must contain at least one lowercase letter
            elif not any(char.islower() for char in password1):
                flash("Password must contain at least one lowercase letter", category='error')
            
            # Password must contain at least one digit
            elif not any(char.isdigit() for char in password1):
                flash("Password must contain at least one digit", category='error')

            # Password must contain at least one special character
            elif not any(char in "!@#$%^&*()_+{}[]|\"'<>,.?/~" for char in password1):
                flash("Password must contain at least one special character", category='error')     

            elif len(password2)==0:
                flash("Please confirm your password", category='error')

            elif password1 != password2:
                flash("The passwords don't match", category='error')

            else:
                new_user = User(email=email, first_name=firstName, password=generate_password_hash(password1, method='sha256'))
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                flash("Account created", category='success')
                return redirect(url_for('views.home'))
        
    return render_template("sign_up.html", user=current_user)    

@auth.route('/renew', methods=['GET', 'POST'])
def renew():
    if request.method == 'POST':
        email = request.form.get('email')
        newPassword1 = request.form.get('newPassword')
        newPassword2 = request.form.get('newPassword2')
        
        user = User.query.filter_by(email=email).first()
        if user:
            user.password = generate_password_hash(newPassword1, method='sha256')
            db.session.commit()
            flash("Password updated successfully", category='success')
            return redirect(url_for('auth.login'))

        else:
            flash("Cannot find user", category='error')

    return render_template('renew.html', user=current_user)