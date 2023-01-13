from app import app
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import SignUpForm, LoginForm, PostForm, AddressForm
from app.models import User, Post, Address

# Welcome
@app.route('/')
def index():
    # address = Address.query.all()
    # return redirect(url_for('index'))
    return render_template('index.html')
    
# Sign Up
@app.route('/signup', methods=["GET", "POST"])
def signup():
    # Create an instance of the SignUpForm
    form = SignUpForm()

    # Check if a SIGNUP request AND data is valid
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

#Login
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
            flash(f"{user.username} logged in", "success")
            return redirect(url_for('address'))
        else:
            flash("Incorrect user and/or password", "danger")
            return redirect(url_for('login'))


    return render_template('login.html', form=form)

# Logout
@app.route('/logout')
def logout():
    logout_user()
    flash("Logged Out", "success")
    return redirect(url_for('index'))

# New Note
@app.route('/create-note', methods = ['GET', 'POST'])
@login_required
def create_note():
    form = PostForm()
    if form.validate_on_submit():
        print('Form Validated!')

        # Get the data
        title = form.title.data
        body = form.body.data
        print(title, body, current_user)

        # Create a new instance for note
        new_post = Post(title=title, body=body, user_id=current_user.id)
        flash(f"\"{new_post.title}\" Note Created", 'success')
        return redirect(url_for('notes'))

    return render_template('addnotes.html', form=form)

# New Address/Contacts
@app.route('/create-contact', methods = ['GET', 'POST'])
@login_required
def create_contact():
    form = AddressForm()
    if form.validate_on_submit():
        print('Form Validated!')

        # Get the data from form
        first_name = form.first_name.data
        last_name = form.last_name.data
        phone = form.phone.data
        address = form.address.data
        print(first_name, last_name, phone, address, current_user)

        # Create a new instance for note
        new_contact = Address(first_name=first_name, last_name=last_name, phone=phone, address=address, user_id=current_user.id)
        flash(f"Contact Added", 'success')
        return redirect(url_for('address'))

    return render_template('newaddress.html', form=form)

# Existing Notes
@app.route('/notes')
@login_required
def notes():
    notes = Post.query.all()
    return render_template('notes.html', notes=notes)

# Existing Address/Contacts
@app.route('/address')
@login_required
def address():
    address = Address.query.all()
    return render_template('addressbook.html', address=address)

# Note ID
@app.route('/notes/<post_id>')
def get_post(post_id):
    # post = Post.query.get_or_404(post_id)
    note = Post.query.get(post_id)
    if not note:
        flash(f"note does not exist")
        return redirect(url_for('notes'))
    return render_template('notes.html', note=note)

# Edit Notes
@app.route('/notes/<post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    note = Post.query.get_or_404(post_id)
    # if not note:
    #     flash(f"A post with id {post_id} does not exist", "danger")
    #     return redirect(url_for('notes'))
    # # Make sure the post author is the current user
    # if note.author != current_user:
    #     flash("You do not have permission to edit this post", "danger")
    #     return redirect(url_for('notes'))
    form = PostForm()
    if form.validate_on_submit():
        # Get the form data
        title = form.title.data
        body = form.body.data
        # update the post using the .update method
        note.update(title=title, body=body)
        flash(f"{note.title} has been updated!", "success")
        return redirect(url_for('notes', post_id=note.id))
    if request.method == 'GET':
        form.title.data = note.title
        form.body.data = note.body
        
    return render_template('editnote.html', note=note, form=form)

# Delete Note
@app.route('/notes/<post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    note = Post.query.get(post_id)
    # if not note:
    #     flash(f"A post with id {post_id} does not exist", "danger")
    #     return redirect(url_for('index'))
    # # Make sure the post author is the current user
    # if note.author != current_user:
    #     flash("You do not have permission to delete this post", "danger")
    #     return redirect(url_for('index'))
    note.delete()
    flash(f"{note.title} has been deleted", "info")
    return redirect(url_for('notes'))

# Contact ID
@app.route('/address/<address_id>')
def get_contact(address_id):
    address = Address.query.get(address_id)
    if not address:
        flash(f"Contact does not exist")
        return redirect(url_for('address'))
    return render_template('addressbook.html', address=address)

# Edit Contact
@app.route('/address/<address_id>/update', methods=['GET', 'POST'])
@login_required
def edit_contact(address_id):
    addy = Address.query.get_or_404(address_id)
    # if not address:
    #     flash(f"A Contact with id {address_id} does not exist", "danger")
    #     return redirect(url_for('address'))
    # # Make sure the post author is the current user
    # if address.author != current_user:
    #     flash("You do not have permission to edit this post", "danger")
    #     return redirect(url_for('address'))
    form = AddressForm()
    if form.validate_on_submit():
        # Get the form data
        first_name = form.first_name.data
        last_name = form.last_name.data
        phone = form.phone.data
        address = form.address.data
        # update the post using the .update method
        addy.update(first_name=first_name, last_name=last_name, phone=phone, address=address)
        flash(f"{addy.first_name} has been updated!", "success")
        return redirect(url_for('address', address_id=addy.id))
    # if request.method == 'GET':
    #     form.first_name.data = address.first_name
    #     form.last_name.data = address.last_name
    #     form.phone.data = address.phone
    #     form.address.data = address.address
        
    return render_template('editcontact.html', addy=addy, form=form)

# Delete Contact
@app.route('/address/<address_id>/delete')
@login_required
def delete_contact(address_id):
    address = Address.query.get(address_id)
    # if not address:
    #     flash(f"A contact with id {address_id} does not exist", "danger")
    #     return redirect(url_for('index'))
    # # Make sure the post author is the current user
    # if address.author != current_user:
    #     flash("You do not have permission to delete this post", "danger")
    #     return redirect(url_for('index'))
    address.delete()
    flash(f"{address.first_name} has been deleted", "info")
    return redirect(url_for('address'))