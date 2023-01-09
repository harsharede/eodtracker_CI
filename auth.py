from .app import app, db
from .models import User
from functools import wraps
import hashlib
import binascii
import jwt
from flask import request
import datetime
import os
import time


def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return 'Missing auth header', 401
        auth_token = auth_header.split(" ")[1]
        if auth_token is None:
            return 'Invalid auth header', 401
        try:
            if is_token_expired(auth_token):
                return 'Token expired'
            user_id = jwt.decode(auth_token, app.config['SECRET_KEY'], algorithms=['HS256'])['user_id']
            user = User.query.get(user_id)
            if user is None:
                return 'Invalid token', 401
        except Exception as e:
            print(e)
            return 'Invalid token', 401
        return func(*args, **kwargs)

    return wrapper


@app.route('/register', methods=['POST'])
def register():
    # Get the request data
    data = request.get_json()
    username = str(data['username'])
    password = str(data['password'])

    existing_user = User.query.filter_by(username=username).first()
    if existing_user is not None:
        return 'User already exists. To get new access token use /login'
    hashed_password = hash_password(password)

    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    access_token = jwt.encode(
        {'user_id': new_user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=43200)},
        app.config['SECRET_KEY'])
    return access_token


@app.route('/login', methods=['POST'])
def login():
    # Get the request data
    data = request.get_json()
    username = data['username']
    password = data['password']

    # Get the user from the database
    user = User.query.filter_by(username=username).first()
    if user is None:
        return 'Invalid username'

    # Verify the password
    if verify_password(user.password, password):
        # Generate an access token
        access_token = jwt.encode(
            {'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=43200)},
            app.config['SECRET_KEY'])
        # Return the access token to the client
        return access_token
    else:
        return 'Invalid password'


def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password, provided_password):
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


def is_token_expired(token):
    try:
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = decoded_token['user_id']
        exp = decoded_token['exp']


        if exp < int(time.time()):
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
