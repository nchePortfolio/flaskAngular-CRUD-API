from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, abort
)

from main import db
from main.services import member_service
from main.models.user import User

bp = Blueprint('member', __name__, url_prefix='/alifs/api/member')


@bp.before_app_request
def load_logged_in_user():
    username = session.get('username')

    if username is None:
        g.user = None
    else:
        g.user = User.query.filter_by(username=username).first()


@bp.route('/all', methods=['GET'])
def get_all_member():    
    return jsonify(member_service.get_all_members())


@bp.route('<int:id>', methods=['GET'])
def get_member(id):    
    member = member_service.get_member(id)
    if not member:
        abort(404)
    return jsonify({'member': member})


@bp.route('add', methods=['POST'])
def add_member():
    request_data = request.get_json()
    if not request_data:
        abort(400)
    if 'first_name' not in request_data:
        abort(400)
    if 'last_name' not in request_data:
        abort(400)

    response = member_service.add_member(request_data)

    return response


@bp.route('update/<int:id>', methods=['PUT'])
def update_member(id):
    request_data = request.get_json()

    if not True in [x in ['first_name', 'last_name'] for x in request_data]:
        abort(400)

    response = member_service.update_member(id, request_data)

    return response


@bp.route('delete/<int:id>', methods=['DELETE'])
def delete_member(id):
    request_data = request.get_json()
    response = member_service.delete_member(id)

    return response
