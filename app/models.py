from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login

#USER
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    address = db.relationship('Address', backref='author', lazy='dynamic')
    notes = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.password = generate_password_hash(kwargs['password'])
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<User {self.id} | {self.username}>"

    def check_password(self, guess_password):
        return check_password_hash(self.password, guess_password)

# ADDRESS/CONTACTS
class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=True)
    phone = db.Column(db.String(25), nullable=True)
    address = db.Column(db.String(50), nullable=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<Address {self.id} | {self.first_name}>"
    

    #Update for contact
    def update(self, **kwargs):
        #for each key value that comes as a key word
        for key, value in kwargs.items():
            # If key is acceptable
            if key in {'first_name', 'last_name', 'phone', 'address'}:
                # Set the attribute on the instance
                setattr(self, key, value)
        # save the updates to database
        db.session.commit()

    # Delete contact
    def delete(self):
        db.session.delete(self)
        db.session.commit()



# USER LOGIN
@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# NOTES   
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<Post {self.id} | {self.title}>"

    #Update for notes
    def update(self, **kwargs):
        #for each key value that comes as a key word
        for key, value in kwargs.items():
            # If key is acceptable
            if key in {'title', 'body'}:
                # Set the attribute on the instance
                setattr(self, key, value)
        # save the updates to database
        db.session.commit()

    # Delete notes
    def delete(self):
        db.session.delete(self)
        db.session.commit()

