from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import LoginForm, RegisterForm
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash,check_password_hash
from .models import User
from . import db

# Create authentication blueprint
bp = Blueprint('auth', __name__ )

# Register
@bp.route('/register', methods=['GET', 'POST'])
def register():
    register = RegisterForm()
    if register.validate_on_submit():
        uname = register.user_name.data
        pwd = register.password.data
        email = register.email_id.data
        contact_number = register.contact_number.data

        u1 = User.query.filter_by(name=uname).first()
        if u1:
            flash('Username already exists, please login')
            return redirect(url_for('auth.login'))

        pwd_hash = generate_password_hash(pwd)
        new_user = User(
            name=uname,
            password_hash=pwd_hash,
            emailid=email,
            contact_number=contact_number 
        )

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))

    return render_template('user.html', form=register, heading='Register')

# Login
@bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    error = None
    if login_form.validate_on_submit():
        # Get username and password from DB
        emailid = login_form.emailid.data
        password = login_form.password.data
        user = User.query.filter_by(emailid=emailid).first()
        if user is None:
            error = 'Incorrect email'
        elif not check_password_hash(user.password_hash, password):
            error = 'Incorrect password'
        if error is None:
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash(error)
    return render_template('user.html', form=login_form, heading='Login')

# Logout
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('main.index'))
