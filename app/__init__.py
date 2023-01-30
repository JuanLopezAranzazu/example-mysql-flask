from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

db_name = "python-mysql-flask"

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:root123@localhost/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

from app.models import Role
from app import models

def create_roles(roles):
    all_roles = Role.query.all()
    if len(all_roles) > 0:
        return

    all_roles = []
    for index in range(len(roles)):
        role = Role(name=roles[index])
        all_roles.append(role)

    db.session.add_all(all_roles)
    db.session.commit()

with app.app_context():
    db.create_all()
    create_roles(["Admin", "User"])

from app import user_routes

