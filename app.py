#!flask/bin/python
from settings import *
from member import *
from flask import redirect, url_for, abort, make_response


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/')
def index():
    return redirect(url_for('get_members'))


@app.route('/alifs/api/members', methods=['GET'])
def get_members():
    # return jsonify(Member.get_members())
    return jsonify({'members': Member.get_members()})

@app.route('/alifs/api/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = Member.get_member(member_id)
    if not member:
        abort(404)
    return jsonify({'member': Member.get_member(member_id)})


@app.route('/alifs/api/members', methods=['POST'])
def create_member():
    request_data = request.get_json()
    print(request_data)
    if not request_data:
        abort(400)
    if 'first_name' not in request_data:
        abort(400)
    if 'last_name' not in request_data:
        abort(400)

    Member.add_member(
        first_name=request_data['first_name'], 
        last_name=request_data['last_name']
    )

    response = Response({'status': 'Member created'}, 201, mimetype='application/json')

    return response


@app.route('/alifs/api/members/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    request_data = request.get_json()
    if not request_data:
        abort(400)

    Member.update_member(
        member_id, 
        first_name=request_data['first_name'], 
        last_name=request_data['last_name']
    )

    response = Response({'status': 'Member updated'}, 201, mimetype='application/json')

    return response


@app.route('/alifs/api/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    Member.delete_member(member_id)
    response = Response({'status': 'Member deleted'}, 201, mimetype='application/json')

    return response


if __name__ == '__main__':
    app.run(debug=True)