from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, abort, make_response
)

from main import db
from main.services import user_service
from main.models.user import User

bp = Blueprint('user', __name__, url_prefix='/alifs/api/auth')


@bp.before_app_request
def load_logged_in_user():
    username = session.get('username')

    if username is None:
        g.user = None
    else:
        g.user = User.query.filter_by(username=username).first()


@bp.route('/all', methods=['GET'])
def get_all_users():    
    return jsonify(user_service.get_all_users())


@bp.route('<string:username>', methods=['GET'])
def get_user(username):    
    user = user_service.get_user(username)
    if not user:
        abort(404)
    return jsonify({'user': user})


@bp.route('register', methods=['POST'])
def register_user():
    request_data = request.get_json()
    if not request_data:
        abort(400)
    if 'email' not in request_data:
        abort(400)
    if 'username' not in request_data:
        abort(400)
    if 'password' not in request_data:
        abort(400)

    if 'admin' not in request_data:
        request_data['admin'] = False

    response = user_service.register_user(request_data)

    return response


@bp.route('login', methods=['POST'])
def log_user():
    request_data = request.get_json()

    if 'username' not in request_data:
        abort(400)
    if 'password' not in request_data:
        abort(400)

    response = user_service.log_user(request_data)

    return response


@bp.route('/logout')
def logout():
    auth_token = parse_auth_header(request)

    response = user_service.logout(auth_token)

    return response


@bp.route('/status', methods=['GET'])
def user_status():
    auth_token = parse_auth_header(request)

    response = user_service.get_user_status(auth_token)

    return response


def parse_auth_header(request):
    # get the auth token
    auth_header = request.headers.get('Authorization')
    if auth_header:
        try:
            auth_token = auth_header.split(" ")[1]
        except:
            responseObject = {
                'status': 'fail',
                'message': 'Bearer token malformed.'
            }
            return make_response(jsonify(responseObject)), 401
    else:
        auth_token = ''

    return auth_token