from sqlite3 import Connection as SQLite3Connection
from datetime import datetime
from sqlalchemy import event
from sqlalchemy.engine import Engine
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import csv
import json
import os

# app
app = Flask(__name__)

file_path = os.path.abspath(os.getcwd())+"\database.db"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///'+file_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = 0

###
#Filling the JSON file with Date Price Open High Low 
columns = ['Date', 'Price', 'Open', 'High', 'Low', "Vol.", "Change %"]
file_csv = open('BTC_USD-Bitfinex-Historical-Data.csv', 'r')
reader = csv.DictReader(file_csv, columns)
file_json = open('affichage.json', 'w')
L = list(reader)
for i in range(1,len(L)) :
    del L[i]["Vol."]
    del L[i]["Change %"]
    json.dump(L[i], file_json, indent=0)

file_csv.close()
file_json.close()

#Affiche tout
#json.dumps(list(csv.reader(open('BTC_USD-Bitfinex-Historical-Data.csv'))))

@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


db = SQLAlchemy(app)
now = datetime.now()

# Model
class bitcoin(db.Model) :
    __tablename__ = "bitcoin"
    Date = db.Column(db.Date, primary_key=True)
    Price = db.Column(db.Float)
    Open = db.Column(db.Float)
    High = db.Column(db.Float)
    Low = db.Column(db.Float)


@app.route("/")
def home():
    return "<h1>API Running</h1>"

        
# routes
@app.route("/bitcoin", methods=['GET', 'POST'])
def create_bitcoin():
    try :
        if request.method == "POST" :
            data = request.get_json()
            if data is None:
                return jsonify({"error": "missing data, please enter it in the body!" }), 400

            for field in ["Date", "Price", "Open", "High", "Low"]:
                if field not in data.keys():
                    return jsonify({"error": "no " + field + " in data" }), 400
            
            new_data = bitcoin(
                Date = data["Date"],
                Price = data["Price"],
                Open = data["Open"],
                High = data["High"],
                Low = data["Low"],
            )
            db.session.add(new_data)
            db.session.commit()
            return jsonify({"message": "User created"}), 200
        else :
            return render_template('affichage.json')
    except Exception as e:
        return jsonify({"error": "Failed, caught exception " + str(e)}), 400

if __name__ == "__main__":
    db.create_all()
    app.run()
    with app.test_request_context('/bitcoin', method='POST'):
    # now you can do something with the request until the
    # end of the with block, such as basic assertions:
        create_bitcoin()
        assert request.path == '/bitcoin'
        assert request.method == 'POST'


'''
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