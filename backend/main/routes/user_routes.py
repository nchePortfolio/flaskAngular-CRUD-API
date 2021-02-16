from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, abort
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
def add_user():
    request_data = request.get_json()
    if not request_data:
        abort(400)
    if 'email' not in request_data:
        abort(400)
    if 'username' not in request_data:
        abort(400)
    if 'password' not in request_data:
        abort(400)

    response = user_service.add_user(request_data)

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
    response = user_service.log_out()

    return response



