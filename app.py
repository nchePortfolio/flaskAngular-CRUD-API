#!flask/bin/python
from flask import Flask, jsonify, redirect, url_for, abort, make_response, request


members = [
    {
        'id': 1,
        'first_name': 'Toto',
        'last_name': 'Matic'
    },
    {
        'id': 2,
        'first_name': 'Joseph',
        'last_name': 'Hicacement'
    }
]


app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/')
def index():
    return redirect(url_for('get_members'))


@app.route('/alifs/api/members', methods=['GET'])
def get_members():
    return jsonify({'members': members})


@app.route('/alifs/api/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = [member for member in members if member['id'] == member_id]
    if len(member) == 0:
        abort(404)
    return jsonify({'member': member[0]})


@app.route('/alifs/api/members', methods=['POST'])
def create_member():
    if not request.json or not 'first_name' in request.json:
        abort(400)
    member = {
        'id': members[-1]['id'] + 1,
        'first_name': request.json['first_name'],
        'last_name': request.json['last_name'],
    }
    members.append(member)
    return jsonify({'member': member}), 201


@app.route('/alifs/api/members/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    member = [member for member in members if member['id'] == member_id]
    if len(member) == 0:
        abort(404)

    request_data = request.get_json()
    if not request_data:
        abort(400)
    if 'first_name' in request_data and not isinstance(request_data['first_name'], str):
        abort(400)
    if 'last_name' in request_data and not isinstance(request_data['first_name'], str):
        abort(400)
    member[0]['first_name'] = request_data['first_name']
    member[0]['last_name'] = request_data['last_name']
    return  jsonify({'member': member[0]})


@app.route('/alifs/api/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    member = [member for member in members if member['id'] == member_id]
    if len(member) == 0:
        abort(404)
    members.remove(member[0])
    return jsonify({'result': True})


if __name__ == '__main__':
    app.run(debug=True)