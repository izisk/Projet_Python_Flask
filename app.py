from sqlite3 import Connection as SQLite3Connection
from datetime import datetime
from sqlalchemy import event
from sqlalchemy.engine import Engine
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import csv
import json


# app
app = Flask(__name__, template_folder="templates")


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlite:///sqlitedb.file"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = 0



columns = ['Price', 'Open', 'High', 'Low']
data_base_csv = pd.read_csv('BTC_USD-Bitfinex-Historical-Data.csv', names=columns)
data_base_html = data_base_csv.to_html("affichage.html")

db = SQLAlchemy(app)
now = datetime.now()

# Model
"""
class data(db.Model) :
    __tablename__ = "data"
    Date = db.column(db.Date)
    Price = db.column(db.Float)
    Open = db.column(db.Float)
    High = db.column(db.Float)
    Low = db.column(db.Float)
"""

@app.route("/")
def home():
    return render_template("affichage.html")


if __name__ == "__main__":
    #db.create_all()
    app.run()
    

"""


# configure sqlite3 to enforce foreign key contraints
'''
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()
'''
    
'''
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    posts = db.relationship("BlogPost", cascade="all, delete")


class BlogPost(db.Model):
    __tablename__ = "blog_post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.String(200))
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
'''
    
# routes
'''
@app.route("/user", methods=["POST"])
def create_user():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "missing data, please enter it in the body!" }), 400

        for field in ["name", "email", "address", "phone"]:
            if field not in data.keys():
                return jsonify({"error": "no " + field + " in data" }), 400
        
        new_user = User(
            name=data["name"],
            email=data["email"],
            address=data["address"],
            phone=data["phone"],
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created"}), 200
    except Exception as e:
        return jsonify({"error": "Failed, caught exception" + str(e)}), 400


@app.route("/user/descending_id", methods=["GET"])
def get_all_users_descending():
    users = User.query.all()
    all_users_ll = linked_list.LinkedList()

    for user in users:
        all_users_ll.insert_beginning(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone,
            }
        )

    return jsonify(all_users_ll.to_list()), 200


@app.route("/user/ascending_id", methods=["GET"])
def get_all_users_ascending():
    users = User.query.all()
    all_users_ll = linked_list.LinkedList()

    for user in users:
        all_users_ll.insert_at_end(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone,
            }
        )

    return jsonify(all_users_ll.to_list()), 200
'''

"""