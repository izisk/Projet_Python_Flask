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
from json2html import *
import io
import plotly
import plotly.express as px


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
    df = pd.read_csv('BTC_USD Bitfinex Historical Data.csv')
    df = df.drop('Vol.', 1)
    df = df.drop('Change %', 1)
    df['Date'] = pd.to_datetime(df['Date'], format='%b %d, %Y')
    df['Price'] = df['Price'].str.replace(',', '').astype(float)
    df['Open'] = df['Open'].str.replace(',', '').astype(float)
    df['High'] = df['High'].str.replace(',', '').astype(float)
    df['Low'] = df['Low'].str.replace(',', '').astype(float)
    leplot = px.line(df, x='Date', y='Price', title= 'Evolution du prix du Bitcoin en fonction du temps')
    graphJSON = json.dumps(leplot, cls=plotly.utils.PlotlyJSONEncoder)
    #return data_html
    return render_template('plot_bitcoin.html', graphJSON=graphJSON)

@app.route("/data_bitcoin")
def data_bitcoin():
    return data_html



if __name__ == "__main__":
    #db.create_all()
    app.run(debug=False)
    #with app.test_request_context('/bitcoin', method='POST'):
    # now you can do something with the request until the
    # end of the with block, such as basic assertions:
        #create_bitcoin()
        #assert request.path == '/bitcoin'
        #assert request.method == 'POST'


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
