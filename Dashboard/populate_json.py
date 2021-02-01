#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Bauyrzhan Ospan"
__copyright__ = "Copyright 2021"
__version__ = "1.0.1"
__maintainer__ = "Bauyrzhan Ospan"
__email__ = "dr.cleverest@gmail.com"
__status__ = "Development"

from glob import glob
from datetime import datetime
import json

names = glob("./static/image/*")

points = []
num = 1

for name in names:
    point_name = name.split("./static/image/")[1].split("-")[0]
    file_name = name
    print(file_name)
    NAME = name.split("./static/image/")[1].split("-")[0]
    MAC = name.split("-")[1]
    file_name = name[2:-1]+"g"
    if NAME[0] == "S":
        FLOOR = "2"
    else:
        FLOOR = NAME.split(".")[1][0]
    BLOCK = NAME.split(".")[0]
    ID = name.split("-")[-1].split('.')[0]
    DATE = datetime.utcfromtimestamp(int(ID)+6*60*60)
    points.append({
        "name": NAME,
        "id": ID,
        "code": MAC,
        "block": BLOCK,
        "floor": FLOOR,
        "datetime": int(ID)+6*60*60,
        "russian_name": "",
        "english_name": "",
        "qazaq_name": "",
        "owner_ru": "",
        "owner_qz": "",
        "owner_en": "",
        "alts": "",
        "phone": "",
        "room": "",
        "filename": file_name.split("/")[-1]
    })


with open('data.json', 'w') as fout:
    json.dump(points , fout)