import os
import secrets
from PIL import Image
from werkzeug.utils import secure_filename
from flask import render_template, url_for, flash, redirect, request
from datetime import datetime, timezone
from flask_login import current_user, login_user, login_required, logout_user, current_user
from app import app, db
from app.forms import RegistrationForm, LoginForm, EditAccountForm,PostForm 
from app.models import User, Post, Image

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
    # Query to get all posts, ordered by latest created first
    posts = Post.query.order_by(Post.created_at.desc()).all()
    
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


@app.route('/create_post', methods=['GET','POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(
            description=form.description.data,
            status=form.status.data,
            country=form.country.data,
            state=form.state.data,
            city=form.city.data,
            address=form.address.data,
            user_id=current_user.id
        )
        db.session.add(new_post)
        db.session.commit()

        if form.photos.data:
            if allowed_images(form.photos.data):
                image_list = save_images(form.photos.data)

                image = Image(filename=image_list, post_id=Post.id)
                db.session.add(image)
                db.session.commit()
        db.session.commit()
        flash('post created successfuly')
        return redirect(url_for('home'))
    return render_template('posts_form.html', title='post page', form=form)



@app.route('/edit_account/', methods=['GET', 'POST'])
@login_required
def edit_account():
    form = EditAccountForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.username = form.username.data
        current_user.phone_number = form.phone_number.data
        current_user.phone_number_2 = form.phone_number_2.data
        db.session.commit()
        flash('your changes has been saved')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.username.data = current_user.username
        form.phone_number.data = current_user.phone_number
        form.phone_number_2.data = current_user.phone_number_2
    return render_template('edit_account.html', title='account page', form=form)

def save_images(form_images):
    """
    rename, resize and save the images and then
    return a list of saved images
    """
    image_list = []

    for form_image in form_images:

        # generate a random hex name for each image
        filename = secure_filename(form_image.filename)
        random_hex_name = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_image.filename)
        new_image_name = '{}.{}'.format(random_hex_name, f_ext)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], new_image_name)

        # resize the image using pillow lib
        new_image_size = (250, 250)
        image = Image.open(form_image)
        image.thumbnail(new_image_size)
        image.save(image_path)

        # append the new filename to the list
        image_list.append(new_image_name)

    return image_list

def allowed_images(image_names):
    """
    check if image has the required extension
    """
    for image_name in image_names:
        if '.' in image_name:
            ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
            image_name_list = image_name.rsplit('.', 1)
            f_ext = image_name_list[1].lower()
            if f_ext in ALLOWED_EXTENSIONS:
                return True
            else:
                return False
        return False


@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    # Retrieve the post to be edited
    post = Post.query.get_or_404(post_id)

    # Check if the current user is authorized to edit the post
    if post.user_id != current_user.id and not current_user.is_admin:
        flash('You are not authorized to edit this post.', 'danger')
        return redirect(url_for('home'))

    form = PostForm(obj=post)

    if form.validate_on_submit():
        # Update post with form data
        post.description = form.description.data
        post.status = form.status.data
        post.country = form.country.data
        post.state = form.state.data
        post.city = form.city.data
        post.address = form.address.data

        # Save any new images
        if form.photos.data:
            if allowed_images([photo.filename for photo in form.photos.data]):
                image_list = save_images(form.photos.data)
                # Delete old images or handle image updates if needed
                # Append new images to the post
                for image_filename in image_list:
                    image = Image(filename=image_filename, post_id=post.id)
                    db.session.add(image)

        db.session.commit()
        flash('Post updated successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('edit_post.html', title='Edit Post', form=form, post=post)