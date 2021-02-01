#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Bauyrzhan Ospan"
__copyright__ = "Copyright 2018, KazPostBot"
__version__ = "1.0.1"
__maintainer__ = "Bauyrzhan Ospan"
__email__ = "bospan@cleverest.tech"
__status__ = "Development"


from gevent import monkey
monkey.patch_all()


from flask import Flask, render_template, request, Markup, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room, \
	close_room, rooms, disconnect
import time
import random
from random import sample
from datetime import datetime
import socket
import json
from pymongo import MongoClient
import pymongo
import requests
from requests import Request, Session
from threading import Lock
import logging
from flask_basicauth import BasicAuth
from glob import glob


async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()
app.config['JSON_AS_ASCII'] = False
app.config['BASIC_AUTH_USERNAME'] = 'NU'
app.config['BASIC_AUTH_PASSWORD'] = 'WeRzeB3st'
basic_auth = BasicAuth(app)
client = MongoClient('mongodb://database:27017/')
logging.basicConfig(level=logging.WARNING)


template = '''
        <tr>
            <td>ID</td>
            <td><img data-enlargeable style="cursor: zoom-in" src="PATH" height="50px"></td>
            <td>Name: NAME<br>Code: MAC<br>Block: BLOCK<br>Floor: FLOOR<br>Date installed: DATE</td>
            <td>
                Room number: <p id='MAC+rn' contenteditable="true" class="w3-border w3-padding">room</p><br>
                Room name RU: <p id='MAC+rnam' contenteditable="true" class="w3-border w3-padding">russian_name</p><br>
                Room name KZ: <p id='MAC+qnam' contenteditable="true" class="w3-border w3-padding">qazaq_name</p><br>
                Room name EN: <p id='MAC+enam' contenteditable="true" class="w3-border w3-padding">english_name</p><br>
                Owners names RU: <p id='MAC+row' contenteditable="true" class="w3-border w3-padding">owner_ru</p><br>
                Owners names KZ: <p id='MAC+qow' contenteditable="true" class="w3-border w3-padding">owner_qz</p><br>
                Owners names EN: <p id='MAC+eow' contenteditable="true" class="w3-border w3-padding">owner_en</p><br>
                Alternative names: <p id='MAC+al' contenteditable="true" class="w3-border w3-padding">alts</p><br>
                Phone number: <p id='MAC+ph' contenteditable="true" class="w3-border w3-padding">phone</p><br>
                <button id='but+MAC' type="button" class="w3-button w3-theme"><i class="fa fa-pencil"></i> Save changes</button> 
            </td>
        </tr>
'''


def read_json():
    with open('data.json', "r") as json_file:
        data = json.load(json_file)
        return data


def write_json(points):
    with open('data.json', 'w') as fout:
        json.dump(points , fout)


def json_to_html():

    all = ""
    data = read_json()
    names = glob("./static/image/*")
    for i in range(len(data)):
        DATE = datetime.utcfromtimestamp(int(data[i]["datetime"])).strftime('%Y-%m-%d %H:%M:%S')
        path = [m for m in names if m.startswith(str(data[i]["name"]))]
        template1 = template
        template1 = template1.replace("ID", str(data[i]["id"]))
        template1 = template1.replace("DATE", str(DATE))
        template1 = template1.replace("MAC", str(data[i]["code"]))
        template1 = template1.replace("NAME", str(data[i]["name"]))
        template1 = template1.replace("BLOCK", str(data[i]["block"]))
        template1 = template1.replace("FLOOR", str(data[i]["floor"])) 
        template1 = template1.replace("PATH", "/static/image/" + str(data[i]["filename"]))

        template1 = template1.replace("room", str(data[i]["room"]))
        template1 = template1.replace("russian_name", str(data[i]["russian_name"]))
        template1 = template1.replace("qazaq_name", str(data[i]["qazaq_name"]))
        template1 = template1.replace("english_name", str(data[i]["english_name"]))
        template1 = template1.replace("owner_ru", str(data[i]["owner_ru"]))
        template1 = template1.replace("owner_qz", str(data[i]["owner_qz"]))
        template1 = template1.replace("owner_en", str(data[i]["owner_en"]))
        template1 = template1.replace("alts", str(data[i]["alts"]))
        template1 = template1.replace("phone", str(data[i]["phone"]))
        all = all + template1
    return all

@app.route("/", methods=["GET", "POST"])
@basic_auth.required
def index():
    table = Markup(json_to_html())
    return render_template(
        "index.html", **locals())

@app.route("/post", methods=["GET", "POST"])
@basic_auth.required
def post():
    data = read_json()
    for i in range(len(data)):
        if str(data[i]["code"]).lower() == str(request.args["mac"]).lower():
            data[i]["room"] = request.args["room"]
            data[i]["russian_name"] = request.args["russian_name"]
            data[i]["qazaq_name"] = request.args["qazaq_name"]
            data[i]["english_name"] = request.args["english_name"]
            data[i]["owner_ru"] = request.args["owner_ru"]
            data[i]["owner_qz"] = request.args["owner_qz"]
            data[i]["owner_en"] = request.args["owner_en"]
            data[i]["alts"] = request.args["alts"]
            data[i]["phone"] = request.args["phone"]
    write_json(data)

    table = Markup(json_to_html())
    return render_template(
        "index.html", **locals())


# Main flask app
if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)