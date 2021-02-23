import datetime

from flask import make_response, jsonify, session

from main import db
from main.models.user import User
from main.models.token import BlacklistToken


def serialize(model):
    return {
        'id': model.id,
        'email': model.email,
        'username': model.username,
        'password': model.password_hash,
        'admin': model.admin,
        'registered_on': model.registered_on,
    }


def register_user(data):
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        try:
            new_user = User(
                email=data['email'],
                username=data['username'],
                password=data['password'],
                admin=data['admin'],
                registered_on=datetime.datetime.utcnow()
            )
            save_changes(new_user)
            auth_token = new_user.encode_auth_token(new_user.id)

            response_object = {
                'status': 'success',
                'message': 'Successfully registered.',
                'auth_token': auth_token
            }

            return make_response(jsonify(response_object), 201)

        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }
            return make_response(jsonify(responseObject), 401)
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }

        return make_response(jsonify(response_object), 202)


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
        auth_token = user.encode_auth_token(user.id)

        if not auth_token:
            response_object = {
                'response': {
                    'status': 'fail',
                    'message': 'Fail to log in: invalid token',
                },
                'status_code': 202
            }
            return make_response(jsonify(response_object['response']), response_object['status_code'])

        if not user.check_password(data['password']):
            response_object = {
                'response': {
                    'status': 'fail',
                    'message': 'Fail to log in: incorrect password',
                },
                'status_code': 202
            }
            return make_response(jsonify(response_object['response']), response_object['status_code'])

        if user.check_password(data['password']) and auth_token:
            session['is_auth'] = True
            print(session)
            user_details = serialize(user)
            user_details['token'] = auth_token

            response_object = {
                'response': {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'user': user_details,
                },
                'status_code': 200
            }
        else:
            response_object = {
                'response': {
                    'status': 'fail',
                    'message': 'Fail to log in: unknown error',
                },
                'status_code': 202
            }
    else:
        response_object = {
            'response': {
                'status': 'fail',
                'message': 'Fail to log in: username {} does not exist'.format(data['username']),
            },
            'status_code': 404
        }

    return make_response(jsonify(response_object['response']), response_object['status_code'])


def logout(auth_token):
    if auth_token:
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            # mark the token as blacklisted
            blacklist_token = BlacklistToken(token=auth_token)
            try:
                # insert the token
                db.session.add(blacklist_token)
                db.session.commit()
                session.pop('is_auth', None)
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully logged out.'
                }
                return make_response(jsonify(responseObject)), 200
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': e
                }
                return make_response(jsonify(responseObject)), 200
        else:
            responseObject = {
                'status': 'fail',
                'message': resp
            }
            return make_response(jsonify(responseObject)), 401
    else:
        responseObject = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        return make_response(jsonify(responseObject)), 403


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


def get_user_status(auth_token):
    # get the auth token
    if auth_token:
        resp = User.decode_auth_token(auth_token)  # resp is user_id (from payload['sub'] in User model)
        if not isinstance(resp, str):
            user = User.query.filter_by(id=resp).first()
            responseObject = {
                'status': 'success',
                'data': {
                    'user_id': user.id,
                    'email': user.email,
                    'username': user.username,
                    'admin': user.admin,
                    'registered_on': user.registered_on
                }
            }
            return make_response(jsonify(responseObject)), 200
        responseObject = {
            'status': 'fail',
            'message': resp
        }
        return make_response(jsonify(responseObject)), 401
    else:
        responseObject = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        return make_response(jsonify(responseObject)), 401


def save_changes(model):
    db.session.add(model)
    db.session.commit()