from flask import Flask, request
import mysql.connector
import math
import requests
import posixpath
import os
import hashlib
import time
import datetime
from datetime import timedelta
import math
from math import cos, pi,sin,acos 
import threading
from time import sleep
from cryptography.fernet import Fernet
from Crypto.Cipher import AES
from apscheduler.schedulers.background import BackgroundScheduler
import json
from flask import jsonify
from flask import Response

import psycopg2
try: 
 conn = psycopg2.connect(database="platdb", user="postgres", password="bat123", host="localhost")
 print("connected")
except:
 print ("I am unable to connect to the database")
mycursor =conn.cursor()

app = Flask(__name__)


@app.route('/')
def index():
    return 'Server Works!'

@app.route('/authServer', methods=['POST'])
def authServer():
    
    input = request.get_json()
    print(input)
    vmdID=input['vmdID']
    username=input['username']
    encrypted_password=input['encrypted_password'] 
    driver_id=input['driver_id'] 
    latitude=input['latitude'] 
    longitude=input['longitude']

    result = mycursor.execute("SELECT vmd_id,username FROM auth where vmd_id=%s",(vmdID,))
    result = mycursor.fetchall()
    for row in result :
        vmdID2=row[0]
        username2=row[1]
        
    try:
        vmdID2
    except NameError:
        return 'VMD not identified'

    answer = mycursor.execute("SELECT driver_vehicle_category FROM driver where driver_id=%s",(driver_id,))
    answer = mycursor.fetchall()
    for row in answer :
        driver_vehicle_category=row[0]

    sol = mycursor.execute("SELECT v_category FROM vehicle where vmd_id=%s",(vmdID,))
    sol = mycursor.fetchall()
    for row in sol :
        v_category=row[0]
    try:   
        ekey="2eEGqWWnclI-W1ILDyG5gXfLAisa7Sc93shTEggZ2CQ="
        f= Fernet(ekey)    
        arr = bytes(encrypted_password, 'utf-8')
        obj3 = f.decrypt(arr)
        usn=obj3.decode("utf-8") 
        print(usn)
        print(v_category)
    except Exception as e:
        return 'Incorrect password'

    try:
        driver_vehicle_category
    except NameError:
        return 'Invalid driver license'

    if driver_vehicle_category==v_category:
        d=1
    else:
        return 'Driver not allowed to drive this type of vehicle'

    if username==usn and d==1:
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        curr_timestamp=timestamp
        #curr_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S') 
        print(timestamp)

        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        hour = time.strftime("%H", t)
        print(current_time)

        t_hours_from_now = datetime.datetime.now() + datetime.timedelta(hours=3)
        expiry_time=t_hours_from_now
        exp_time=t_hours_from_now.isoformat()
        print(exp_time)
        ext=t_hours_from_now.replace(microsecond=0)
        #expiry_timestamp = t_hours_from_now.strftime('%Y-%m-%d %H:%M:%S') 
        print(ext)

        curr_time=datetime.datetime.now().isoformat()
        print(curr_time)
      
        data = {"timestamp": curr_time ,  
                "exp_time": exp_time,  
                "port":"6002"}

        mycursor.execute("INSERT into vmd_timestamp(vmd_id, curr_timestamp, expiry_time) values(%s, %s,%s)", (vmdID, curr_timestamp, expiry_time,))
        conn.commit()

        jsdata = json.dumps(data)

      
        return jsdata
    else:
        return 'Service cannot be accessed'


