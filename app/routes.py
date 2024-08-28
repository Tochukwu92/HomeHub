from flask import render_template
from app import app
from app.forms import RegistrationForm, LoginForm
from config import Config

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

@app.route('/register/')
def register():
    form = RegistrationForm()
    return render_template('register.html', title='register', form=form)

@app.route('/login/')
def login():
    form = LoginForm()
    return render_template('login.html', title='login', form=form)