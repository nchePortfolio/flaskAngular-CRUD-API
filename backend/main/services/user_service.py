import datetime

from flask import make_response, jsonify, session

from main import db
from main.models.user import User


def serialize(model):
    return {
        'id': model.id,
        'email': model.email,
        'username': model.username,
        'password': model.password_hash,
        'admin': model.admin,
        'registered_on': model.registered_on,
    }


def add_user(data):
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        new_user = User(
            email=data['email'],
            username=data['username'],
            password=data['password_hash'],
            admin=data['admin'],
            registered_on=datetime.datetime.utcnow()
        )
        save_changes(new_user)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.'
        }
        return make_response(jsonify(response_object), 201)
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return make_response(jsonify(response_object), 409)


def log_user(data):
    response_object = {
        'response': {
            'status': 'fail',
            'message': 'Invalid login request.'
        },
        'status_code': 409
    }

    user = User.query.filter_by(username=data['username']).first()
    if user:
        if user.check_password(data['password']):
            session['logged_in'] = True
            session['username'] = data['username']

            response_object = {
                'response': {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                },
                'status_code': 201
            }
        else:
            response_object = {
                'response': {
                    'status': 'fail',
                    'message': 'Fail to log in: incorrect password',
                },
                'status_code': 400
            }
    else:
        response_object = {
            'response': {
                'status': 'fail',
                'message': 'Fail to log in: username {} does not exist'.format(data['username']),
            },
            'status_code': 400
        }

    return make_response(jsonify(response_object['response']), response_object['status_code'])


def log_out():
    response_object = {
        'response': {
            'status': 'success',
            'message': 'Successfully logged out.',
        },
        'status_code': 201
    }

    session.clear()

    return make_response(jsonify(response_object['response']), response_object['status_code'])    


def get_all_users():
    return [serialize(user) for user in User.query.all()]


def get_user(username):
    user = User.query.filter_by(username=username).first()
    return serialize(user)


def add_user(data):
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        new_user = User(
            email=data['email'],
            username=data['username'],
            password=data['password_hash'],
            admin=data['admin'],
            registered_on=datetime.datetime.utcnow()
        )
        save_changes(new_user)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.'
        }
        return make_response(jsonify(response_object), 201)
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return make_response(jsonify(response_object), 409)


def update_user(data):
    """
    @TODO check if new username is unique
    """
    has_changed = False

    response_object = {
        'response': {
            'status': 'error',
            'message': 'Fail to update requested user.'
        },
        'status_code': 409
    }

    user_to_update = User.query.filter_by(username=data['username']).first()

    if data['email']:
        user_to_update.email = data['email']
        has_changed = True
    if data['username']:
        user_to_update.username = data['username']
        has_changed = True
    if data['password']:
        user_to_update.password = data['password']
        has_changed = True
    if data['admin']:
        user_to_update.admin = data['admin']
        has_changed = True

    if has_changed:
        db.session.commit()

        response_object = {
            'response': {
                'status': 'success',
                'message': 'Successfully updated user {}'.format(data['username'])
            },
            'status_code': 201
        }

    return make_response(jsonify(response_object['response']), response_object['status_code'])    


def delete_user(id):
    response_object = {
        'response': {
            'status': 'error',
            'message': 'Fail to delete requested user.'
        },
        'status_code': 409
    }

    user_to_delete = User.query.filter_by(id=id)

    if user_to_delete:
        user_to_delete.delete()
        db.session.commit()

        response_object = {
            'response': {
                'status': 'success',
                'message': 'Successfully deleted user id {}'.format(id)
            },
            'status_code': 201
        }

    return make_response(jsonify(response_object['response']), response_object['status_code'])    


def save_changes(model):
    db.session.add(model)
    db.session.commit()