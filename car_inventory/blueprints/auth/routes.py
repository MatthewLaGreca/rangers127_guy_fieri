from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user

from forms import RegisterForm, LoginForm
from models import User, db

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():

    registerform = RegisterForm()

    if request.method == 'POST' and registerform.validate_on_submit():
        first_name = registerform.first_name.data
        last_name = registerform.last_name.data
        username = registerform.username.data
        email = registerform.email.data
        password = registerform.password.data

        if User.query.filter(User.username == username).first():
            flash('Username already exists, try another', category='warning')
            return redirect('/signup')

        if User.query.filter(User.email == email).first():
            flash('Email is already being used, try another', category='warning')
            return redirect('/signup')
        
        user = User(username, email, password, first_name=first_name, last_name=last_name)

        db.session.add(user)
        db.session.commit()

        flash(f'You have successfully registered with username {username}', category='success')
        return redirect('/signin')
    
    return render_template('sign_up.html', form=registerform)