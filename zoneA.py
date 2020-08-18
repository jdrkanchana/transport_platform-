from flask import Flask, request
import mysql.connector
import math
import requests
import posixpath
import os
import hashlib
import time
import datetime
#import thread
import threading
from time import sleep
from apscheduler.schedulers.background import BackgroundScheduler

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="bat123",
    database="platdb"
)
mycursor = mydb.cursor()

zoneA_capacity=0
a=0

app = Flask(__name__)

node_ip = "127.0.0.1:5001"
port = 5001
zone_region ="Colombo"

@app.route('/')
def index():
    return 'Server Works!'

@app.route('/zone', methods=['POST'])
def zone():
    input = request.get_json()
    print(input)
    latitude=input['latitude'] 
    longitude=input['longitude']
    vmd_id=input['vmd_id']

    answer = mycursor.execute("SELECT curr_timestamp, expiry_time FROM vmd_timestamp where vmd_id=%s",(vmdID,))
    answer = mycursor.fetchall()
    for row in answer :
        curr_timestamp=row[0]
        exp_time=row[1]

    tims = time.time()
    current_timestamped = datetime.datetime.fromtimestamp(tims).strftime('%Y-%m-%d %H:%M:%S') 
    current_timestamped2=datetime.datetime.strptime(current_timestamped,'%Y-%m-%d %H:%M:%S')
    
    t = time.localtime()
    exp_hour = time.strftime("%H", t)
    expiry_hour=int(exp_hour)

    global a
    if exp_time>current_timestamped2: 
    #and expiry_hour<=22:
        a=1
   # if exp_time<current_timestamped2 and expiry_hour>22:
        a=1
    else:
        a=0
   
    if a==1:
        global zoneA_capacity
        if zoneA_capacity<3000 and contingency_zone==1:
            print("connected")
            zoneA_capacity=zoneA_capacity+1
            print(zoneA_capacity)
            zone_capacity=zoneA_capacity
            mycursor.execute("INSERT into zoneCapacity(node_ip,port,zone_region,zone_capacity,current_timestamped ) values(%s, %s,%s,%s,%s)", (node_ip,port,zone_region,zone_capacity,current_timestamped))
            conn.commit()
            return {"status":"connected"}

        elif zoneA_capacity<3000 :
            print("connected")
            zoneA_capacity=zoneA_capacity+1
            print(zoneA_capacity)
            zone_capacity=zoneA_capacity
            mycursor.execute("INSERT into vmdContingencyZone(node_ip,port,zone_region,vmdID,current_timestamped ) values(%s, %s,%s,%s,%s)", (node_ip,port,zone_region,vmdID,current_timestamped))
            conn.commit()
            mycursor.execute("INSERT into zoneCapacity(node_ip,port,zone_region,zone_capacity,current_timestamped ) values(%s, %s,%s,%s,%s)", (node_ip,port,zone_region,zone_capacity,current_timestamped))
            conn.commit()
            return {"status":"connected"}

        #docker(os)
        else :
            print("connection failed")
            yid=mycursor.execute("SELECT MIN(zone_capacity) AS minimum FROM zoneCapacity")
            yid = cursor.fetchall()
            for row in yid :
                min_zone_capacity=row[0]

            answer = mycursor.execute("SELECT port,zone_region FROM zoneCapacity where zone_capacity=%s",(min_zone_capacity,))
            answer = mycursor.fetchall()
            for row in answer :
                contingency_port=row[0]
                contingency_zone_region=row[1]
                contingency_zone=1
            
            data = {"contingency zone": contingency_zone ,  
                "contingency port": contingency_port,  
                "status":"not connected"}

            jsdata = json.dumps(data)
            return jsdata

    else:
        print("session expired")

    