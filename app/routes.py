from app import app
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import SignUpForm, LoginForm, PostForm
from app.models import User, Post

@app.route('/')
def index():
    return render_template('index.html')
    

@app.route('/signup', methods=["GET", "POST"])
def signup():
    # Create an instance of the SignUpForm
    form = SignUpForm()

    # Check if a POST request AND data is valid
    if form.validate_on_submit():
        print('Form Submitted and Validated!')

        # Get data from the form
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        print(first_name, last_name, email, username, password)

         # Query our user table to see if there are any users with either username or email from form
        check_user = User.query.filter( (User.username == username) | (User.email == email) ).all()

        # If the query comes back with any results
        if check_user:
            # Flash message saying that a user with email/username already exists
            flash('That email and/or username is taken.', 'danger')
            return redirect(url_for('signup'))

         # If check_user is empty, create a new record in the user table
        new_user = User(first_name = first_name, last_name = last_name, email = email, username = username, password = password)

        # Flash a success message
        flash('Thank you {} {} for signing up!'.format(first_name, last_name), 'success')
        
        # Redirect back to Home
        return redirect(url_for('index'))

    return render_template('signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #get the username and password
        username = form.username.data
        password = form.password.data
        print(username, password)

        #Query the user table to see if a user has that username
        user = User.query.filter_by(username=username).first()

        # Check if user and password is correct
        if user is not None and user.check_password(password):

            #log user in
            login_user(user)
            flash(f"{user.username} is logged in", "success")
            return redirect(url_for('index'))
        else:
            flash("Incorrect user and/or password", "danger")


    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash("You have logged out successfully", "success")
    return redirect(url_for('index'))


@app.route('/create-post', methods = ['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        print('Form Validated!')
        # Get the data
        title = form.title.data
        body = form.body.data
        print(title, body, current_user)
        # Create a new instance for post
        new_post = Post(title=title, body=body, user_id=current_user.id)
        flash(f"Post Create", 'success')
        return redirect(url_for('index'))

    return render_template('create.html', form=form)
