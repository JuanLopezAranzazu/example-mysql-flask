from app import app, db
from app.models import User, Role, user_schema, users_schema
from flask import request, jsonify


@app.route('/users', methods=['GET'])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)


@app.route('/users/<id>', methods=['GET'])
def get_a_user(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)


@app.route('/users', methods=['POST'])
def create_user():
    firstname = request.json['firstname']
    lastname = request.json['lastname']
    email = request.json['email']
    roles = request.json['roles']

    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({"message": "User already exists"})

    new_user = User(firstname, lastname, email)

    if len(roles) > 0:
        for index in range(len(roles)):
            role = Role.query.filter_by(name=roles[index]).first()
            new_user.roles.append(role)
    else:
        role = Role.query.filter_by(name="User").first()
        new_user.roles.append(role)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)


@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"message": "User not found"})

    firstname = request.json['firstname']
    lastname = request.json['lastname']
    email = request.json['email']
    roles = request.json['roles']

    user.firstname = firstname
    user.lastname = lastname
    user.email = email
    user.roles = []

    if len(roles) > 0:
        for index in range(len(roles)):
            role = Role.query.filter_by(name=roles[index]).first()
            user.roles.append(role)
    else:
        role = Role.query.filter_by(name="User").first()
        user.roles.append(role)

    db.session.commit()

    return user_schema.jsonify(user)


@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)
