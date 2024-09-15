import os
import secrets
from PIL import Image
from werkzeug.utils import secure_filename
from flask import render_template, url_for, flash, redirect, request, abort
from datetime import datetime, timezone
from flask_login import current_user, login_user, login_required, logout_user, current_user
from app import app, db
from app.forms import RegistrationForm, LoginForm, EditAccountForm 
from app.forms import PostForm
from app.models import User, Post, PostImage



@app.route('/')
@app.route('/home/')
def home():
    # Query to get all posts, ordered by latest created first
    # posts = Post.query.get.all()
    
    return render_template('home.html', title='home page')

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



@app.route('/account/')
@login_required
def account():
    user = User.query.all()
    return render_template('account.html', title='account page', user=user)


@app.route('/posts/new', methods=['GET','POST'])
@login_required
def new_post():
    """
    """
    form = PostForm()
    if form.validate_on_submit():
        print(f"Photos Data: {form.images.data}")
        print(f"Data Type: {type(form.images.data)}")
        # create a new post object
        post = Post(
            description=form.description.data,
            status=form.status.data,
            country=form.country.data,
            state=form.state.data,
            city=form.city.data,
            address=form.address.data,
            user_id=current_user.id,
            agent=current_user
        )
        db.session.add(post)
        db.session.commit()

        # handle image uploads
        if form.images.data:
            if allowed_images(form.images.data):
                image_list = save_images(form.images.data)

                # save each image with the post_id
                for image_filename in image_list:
                    print(f"Images Data: {form.images.data}")
                    print(f"Data Type: {type(form.images.data)}")
                    image = PostImage(filename=image_filename, post_id=post.id)
                    db.session.add(image)
                db.session.commit()
        flash('post created successfuly')
        return redirect(url_for('home'))
    return render_template('posts_form.html', title='post page', form=form)


@app.route('/posts/')
def all_post():
    posts = Post.query.all()
    return render_template('posts.html', title='post page', posts=posts)


@app.route('/posts/<post_id>/')
def single_post(post_id):
    posts = Post.query.get_or_404(post_id)
    return render_template('_posts.html', title='post page', posts=posts)


@app.route('/posts/<post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.agent != current_user:
        abort(403)
    
    form = PostForm(obj=post)
    
    if form.validate_on_submit():
        # Update the post fields with form data
        post.description = form.description.data
        post.status = form.status.data
        post.country = form.country.data
        post.state = form.state.data
        post.city = form.city.data
        post.address = form.address.data
        
        if form.images.data:
            if allowed_images(form.images.data):
                image_list = save_images(form.images.data)
                # Remove old images if necessary
                Image.query.filter_by(post_id=post.id).delete()
                # Add new images
                for image_filename in image_list:
                    image = Image(filename=image_filename, post_id=post.id)
                    db.session.add(image)
        
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('single_post', post_id=post.id))
    
    return render_template('posts_form.html', title='Update Post', form=form)




# @app.route('/posts/<post_id>/update', methods=['GET', 'POST'])
# @login_required
# def update_post(post_id):
#     posts = Post.query.get_or_404(post_id)
#     if posts.agent != current_user:
#         abort(403)
#     form = PostForm()
#     if form.validate_on_submit():
#         posts.description = form.description.data,
#         posts.status = form.status.data,
#         posts.country = form.country.data,
#         posts.state = form.state.data,
#         posts.city = form.city.data,
#         posts.address = form.address.data
#         if form.images.data:
#             if allowed_images(form.images.data):
#                 image_list = save_images(form.images.data)
#                 image = Image(filename=image_list, post_id=posts.id)
#         db.session.commit()
#         flash('your post has been updated!')
#         return redirect(url_for('single_post', post_id=posts.id))
#     elif request.method == 'GET':
#         form.description.data = posts.description
#         form.status.data = posts.status
#         form.country.data = posts.country
#         form.state.data = posts.state
#         form.city.data = posts.city
#         form.address.data = posts.address
#         form.images.data = posts.images
#     return render_template('posts_form.html', title='update_post page', form=form)


@app.route('/posts/<int:post_id>/', methods=['POST'])
@login_required
def delete_post(post_id):
    if request.form.get('_method') == 'delete':
        post = Post.query.get_or_404(post_id)
        if post.agent != current_user:
            abort(403)

        try:
            db.session.delete(post)
            db.session.commit()
            flash('Your post has been successfully deleted!')
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}')

        return redirect(url_for('home'))

# @app.route('/posts/<post_id>/', methods=['DELETE'])
# @login_required
# def delete_post(post_id):
#     posts = Post.query.get_or_404(post_id)
#     print(posts)
#     if posts.agent != current_user:
#         abort(403)
    
#     db.session.delete(posts)
#     db.session.commit()
#     flash('your post has been sucessfully deleted!')
#     return redirect(url_for('home'))


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
    Rename, resize, and save the images and return a list of saved image names.
    """
    image_list = []
    new_image_size = (250, 250)

    for form_image in form_images:

        # generate a random hex name for each image
        filename = secure_filename(form_image.filename)
        random_hex_name = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_image.filename)
        new_image_name = '{}.{}'.format(random_hex_name, f_ext)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], new_image_name)

        # Resize the image using Pillow
        image = Image.open(form_image)
        image.thumbnail(new_image_size)
        image.save(image_path)

        # Append the new filename to the list
        image_list.append(new_image_name)

    return image_list


def allowed_images(image_names):
    """
    check if image has the required extension
    """
    ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
    for image_name in image_names:
        if '.' in image_name:
            image_name_list = image_name.rsplit('.', 1)
            f_ext = image_name_list[1].lower()
            if f_ext not in ALLOWED_EXTENSIONS:
                return False
        return False
    

@app.route('/logout/')
@login_required
def logout():
    """
    """
    logout_user()
    return redirect(url_for('home'))