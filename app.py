from flask import Flask, g, request, jsonify
from db import get_db
from functools import wraps

app = Flask(__name__)

api_username = 'admin'
api_password = 'password'


def protected(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == api_username and auth.password == api_password:
            return f(*args, **kwargs)
        return jsonify({'message': 'Authentication failed'}), 403

    return decorated


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/member', methods=['GET'])
@protected
def get_members():
    db = get_db()
    members_cursor = db.execute('SELECT id, name, email, level from members')
    members_data = members_cursor.fetchall()

    member_list = []
    for id, name, email, level in members_data:
        member_list.append({'id': id, 'name': name,
                            'email': email, 'level': level})

    username = request.authorization.username
    password = request.authorization.password

    return jsonify({'members': member_list})


@app.route('/member/<int:member_id>', methods=['GET'])
@protected
def get_member(member_id):
    db = get_db()
    members_cursor = db.execute('SELECT id, name, email, level from members WHERE id = ?', [member_id])
    member_data = members_cursor.fetchone()

    return jsonify({'member': {'id': member_data['id'], 'name': member_data['name'],
                               'email': member_data['email'], 'level': member_data['level']}})


@app.route('/member', methods=['POST'])
@protected
def add_member():
    new_member = request.get_json()

    db = get_db()
    db.execute("INSERT INTO members (name, email, level) values (?, ?,?)",
               [new_member['name'], new_member['email'], new_member['level']])
    db.commit()

    member_cursor = db.execute('SELECT id, name, email, level FROM members WHERE name = ?', [new_member['name']])
    member_data = member_cursor.fetchone()

    return jsonify({'member': {'id': member_data['id'], 'name': member_data['name'],
                               'email': member_data['email'], 'level': member_data['level']}})


@app.route('/member/<int:member_id>', methods=['PUT', 'PATCH'])
@protected
def edit_member(member_id):
    member_update = request.get_json()
    db = get_db()
    db.execute('UPDATE members SET name = ?, email = ?, level = ? '
               'WHERE id = ?', [member_update['name'], member_update['email'], member_update['level'], member_id])
    db.commit()

    member_cur = db.execute('SELECT id, name, email, level FROM members WHERE id = ?', [member_id])
    member = member_cur.fetchone()

    return jsonify({'member': {'id': member['id'], 'name': member['name'],
                               'email': member['email'], 'level': member['level']}})


@app.route('/member/<int:member_id>', methods=['DELETE'])
@protected
def delete_member(member_id):
    db = get_db()
    db.execute('DELETE FROM members WHERE id = ?', [member_id])
    db.commit()

    return jsonify({'message': 'Member id: {}, has been deleted'.format(member_id)})


if __name__ == '__main__':
    app.run(debug=True)
