from flask import make_response, jsonify, session, abort

from main import db
from main.models.member import Member


def serialize(model):
    return {
        'id': model.id,
        'first_name': model.first_name,
        'last_name': model.last_name,
    }


def get_all_members():
    return [serialize(member) for member in Member.query.all()]


def get_member(id):
    member = Member.query.filter_by(id=id).first()
    if not member:
        abort(400)

    return serialize(member)


def add_member(data):
    response_object = {
        'response': {
            'status': 'error',
            'message': 'Fail to add new member member.'
        },
        'status_code': 409
    }

    member = Member.query.filter_by(
        first_name=data['first_name']).filter_by(
        last_name=data['last_name']).first()

    if not member:
        new_member = Member(first_name=data['first_name'], last_name=data['last_name'])
        save_changes(new_member)

        response_object = {
            'response': {
                'status': 'success',
                'message': 'Successfully created member {} {}.'.format(data['first_name'], data['last_name'])
            },
            'status_code': 201
        }
    else:
        response_object = {
            'response': {
                'status': 'fail',
                'message': 'Member {} {} already exists.'.format(data['first_name'], data['last_name'])
            },
            'status_code': 201
        }

    return make_response(jsonify(response_object['response']), response_object['status_code'])


def update_member(id, data):
    """
    @TODO check if new first_name and last_name are unique
    """
    has_changed = False

    response_object = {
        'response': {
            'status': 'error',
            'message': 'Fail to update requested member.'
        },
        'status_code': 409
    }

    member_to_update = Member.query.filter_by(id=id).first()

    if data['first_name']:
        member_to_update.first_name = data['first_name']
        has_changed = True
    if data['last_name']:
        member_to_update.last_name = data['last_name']
        has_changed = True

    if has_changed:
        db.session.commit()

        response_object = {
            'response': {
                'status': 'success',
                'message': 'Successfully updated member {}'.format(data['first_name'])
            },
            'status_code': 201
        }

    return make_response(jsonify(response_object['response']), response_object['status_code'])    


def delete_member(id):
    response_object = {
        'response': {
            'status': 'error',
            'message': 'Fail to delete requested member.'
        },
        'status_code': 409
    }

    member_to_delete = Member.query.filter_by(id=id)

    if member_to_delete.first():
        member_to_delete.delete()
        db.session.commit()

        response_object = {
            'response': {
                'status': 'success',
                'message': 'Successfully deleted member id {}'.format(id)
            },
            'status_code': 201
        }
    else:
        response_object = {
            'response': {
                'status': 'fail',
                'message': 'Requested member id does not exist.'
            },
            'status_code': 409
        }

    return make_response(jsonify(response_object['response']), response_object['status_code'])    


def save_changes(model):
    db.session.add(model)
    db.session.commit()