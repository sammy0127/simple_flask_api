from flask import Flask, g, request
from db import get_db

app = Flask(__name__)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/member', methods=['GET'])
def get_members():
    return 'This returns all the members'


@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    return "This will return one member by id {}".format(member_id)


@app.route('/member', methods=['POST'])
def add_member():
    new_member = request.get_json()

    db = get_db()
    db.execute("INSERT INTO members (name, email, level) values (?, ?,?)", [new_member['name'], new_member['email'], new_member['level']])
    db.commit()

    return 'recieved data for {}, {}, {}'.format(new_member['name'], new_member['email'], new_member['level'])


@app.route('/member/<int:member_id>', methods=['PUT', 'PATCH'])
def edit_member(member_id):
    return 'this updates a member by id: {}'.format(member_id)


@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    return 'This Removes a member by ID: {}'.format(member_id)


if __name__ == '__main__':
    app.run(debug=True)
