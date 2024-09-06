from flask import render_template, url_for, flash, redirect, request
from datetime import datetime, timezone
from flask_login import current_user, login_user, login_required, logout_user
from app import app, db
from app.forms import RegistrationForm, LoginForm, EditAcountForm
from app.models import User

posts = [
    {
        'agent': 'Michael Joe',
        'discription': 'two bedroom flat',
        'Address': '54 oshodu street',
        'State': 'Lagos',
        'city': 'Lagos',
        'country': 'Nigeria',
        'Photos': '',
        'date_posted': 'Oct 21, 2023',
        'status': 'Not rented',
        'phone number': '0804 084 348'
    }
]

@app.route('/')
@app.route('/home/')
def home():
    return render_template('home.html', title='home page', posts=posts)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

@app.route('/register/', methods=['GET', 'POST'])
def register():
    """
    Handle user registration, create a new user, and redirect to the login page.
    """
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit(): 
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            email=form.email.data,
            phone_number=form.phone_number.data,
            phone_number_2=form.phone_number_2.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account successfully created for {form.username.data}')
        return redirect(url_for('login'))
    return render_template('register.html', title='register', form=form)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    """
    Handle user login, authenticate the user, and redirect to the home page.
    """
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if next_page:
                flash('you have logged in successfully!')
                return redirect(next_page)
            else:
                flash('you have logged in successfully!')
                return redirect(url_for('home'))
        else:
            flash('Incorrect Email or Password')
            return render_template('login.html', title='login form', form=form)
    return render_template('login.html', title='login form', form=form)

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account/')
@login_required
def account():
    #user = User.query.filter_by(username=username).first()
    return render_template('account.html', title='account page')


@app.route('/edit_account/', methods=['GET', 'POST'])
@login_required
def edit_account():
    form = EditAcountForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.username = form.username.data
        current_user.phone_number = form.phone_number.data
        current_user.phone_number_2 = form.phone_number_2.data
        db.session.commit()
        flash('your changes has been saved')
        return redirect(url_for('edit_account'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.username.data = current_user.username
        form.phone_number.data = current_user.phone_number
        form.phone_number_2.data = current_user.phone_number_2
    return render_template('edit_account.html', title='account page', form=form)