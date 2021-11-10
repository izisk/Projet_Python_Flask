from sqlite3 import Connection as SQLite3Connection
from datetime import datetime
from sqlite3.dbapi2 import DatabaseError
from sqlalchemy import event
from sqlalchemy.engine import Engine
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import csv
import json
import os
from json2html import *
import io
import plotly
import plotly.express as px
from datetime import datetime
from dateutil import parser
import numpy as np


try:
    to_unicode = unicode
except NameError:
    to_unicode = str

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
file_json = io.open('affichage.json', 'w', encoding='utf-8')
L = list(reader)
L = L[1::]
for i in range(len(L)) :
    del L[i]["Vol."]
    del L[i]["Change %"]
str_ = json.dumps(L, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
file_json.write(to_unicode(str_))
file_csv.close()
file_json.close()

#Filling the HTML file with the JSON data
file_json_read = open('./affichage.json', 'r')
with open("affichage.json", encoding='utf-8', errors='ignore') as json_data:
     data_json = json.load(json_data, strict=False)
#infoFromJson = json.loads(str(file_json_read))
#print(json2html.convert(data_json))
data_html = json2html.convert(data_json)
file = open("templates/data_bitcoin.html","w")
file.write(data_html)
file.close()
file_json_read.close()


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

# Routes
@app.route("/")
def home():
    return render_template('home.html')
        
@app.route('/plot_bitcoin')
def plot_bitcoin():
    DatePrice = []
    for elem in data_json :
        DatePrice.append([datetime.strptime(str(elem['Date'][::]), "%b %d, %Y").date(), (float(elem['Price'][::].replace(',', '')))])
    DP = np.array(DatePrice)
    leplot = px.line(DP, x= DP[:,0], y= DP[:,1], labels= {'x' : 'Date', 'y' : 'Price'})
    lep = px.line()
    graphJSON = json.dumps(leplot, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('plot_bitcoin.html', graphJSON=graphJSON)


@app.route('/requests', methods= ["POST", "GET"])
def requests():
    if request.method == "POST" :
        date1 = request.form["req1"]
        return redirect(url_for("date1", don1=date1))
    else :
        return render_template("requests.html")
    
# My idea for now for the request 1 (where given a date we want to retrieve corresponding Price Open High Low) 
# is to use a JSON object.

# For the request 2 (where given two dates we want to load all closing prices 
# for that date range and display the last nth element where n is small) 
# is to also use the Json object for retreveing the corresponding prices.
# Then load thoses prices in a a List so that I can sort them fast.
    
@app.route('/<don1>')
def request1(don1):
    return f"<h1>{don1}</h1>"


@app.route("/data_bitcoin")
def data_bitcoin():
    return data_html


if __name__ == "__main__":
    #db.create_all()
    app.run(debug=False)
    


'''
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
'''
