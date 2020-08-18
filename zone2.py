from flask import Flask, request
import mysql.connector
import math
import requests
import time
import datetime
from time import sleep
import json
import math
from math import cos, pi,sin,acos


import psycopg2
try: 
 conn = psycopg2.connect(database="platdb", user="postgres", password="bat123", host="localhost")
 print("connected")
except:
 print ("I am unable to connect to the database")
mycursor =conn.cursor()


d=0
m=0

app = Flask(__name__)

zone_id=1
zone_port=6002
zone_name ="zone1"
zone_lat = 7.513617     #Westen Zone
zone_longtitude = 80.137133

@app.route('/')
def index():
    return 'Server Works!'

@app.route('/zone', methods=['POST'])
def zone():
    input = request.get_json()
    print(input)
    latitude=input['latitude'] 
    longitude=input['longitude']
    vmd_id=input['vmdID']

    ticketvalid=ticketValidation(vmd_id)
    not_expired=ticketvalid
    print(not_expired)
    print("amal")
    insideZ=insideZone(latitude,longitude,vmd_id)
    within_zone=insideZ
#----------------------------------------------------------------------------------
    ans=mycursor.execute("SELECT zone_capacity FROM zone_capacity where zone_port=%s  ", (zone_port,))
    ans =mycursor.fetchall()
    for row in ans :
        zone_capacity=row[0]
        call=zone_capacity
    try:    
        if tcurr_timestamp.time() < zcurr_timestamped.time():
            within_zone=1
        else:
            within_zone=2
    except:
        print("hello")

    if within_zone==1 and not_expired==1:
        ans=mycursor.execute("SELECT zone_capacity FROM zone_capacity where zone_port=%s  ", (zone_port,))
        ans =mycursor.fetchall()
        for row in ans :
            zone_capacity=row[0]
            if zone_capacity<3000 and call>0:
                m=1
            else:
                m=0
        if m==1:
            print("connected")
            
            mycursor.execute("UPDATE zone_capacity SET zone_capacity = zone_capacity + 1  where zone_port=%s",(zone_port,)) 
            
            conn.commit()
            try:
                mycursor.execute("UPDATE zone_available SET zone_capacity = zone_capacity + 1  where zone_port=%s",(zone_port,)) 
                conn.commit()
            except:
                return hello

            #mycursor.execute("INSERT into zone_available(zone_id , zone_port , zone_name , zone_capacity )values(%s, %s,%s,%s)", (zone_id , zone_port , zone_name , zone_capacity,))
            #conn.commit()
            return {"status":"connected"}
        elif m==0:
            return{"status":"capacity full"}
#-----------------zone transfer--------------------------
    elif within_zone==0:
        mycursor.execute("DELETE FROM vmd_timestamp where vmd_id=%s", (vmd_id,))
        conn.commit()

        try:
            mycursor.execute("DELETE FROM vmdLocalZone where vmd_id=%s", (vmd_id,))
            conn.commit()
        except:
            mycursor.execute("DELETE FROM vmdContingencyZone where vmd_id=%s", (vmd_id,))
            conn.commit()

       
        print("out of the zone, please get connect to new zone from central")
        data = {"central port": "5001", "ticket status":"zone transfer"}
        jsdata = json.dumps(data)
        return jsdata


        #docker(os)      
#--------------------tickets expiry-------------------------
    else:
        try:
            try:
                mycursor.execute("DELETE FROM vmd_timestamp where vmd_id=%s", (vmd_id),)
                conn.commit()
            except:
                print("no prior VMD timestamp record")
            try:
                mycursor.execute("DELETE FROM vmdLocalZone where vmd_id=%s", (vmd_id),)
                conn.commit()
            except:
                print("no assigned local zone")
            try:
                mycursor.execute("DELETE FROM vmdContingencyZone where vmd_id=%s", (vmd_id),)
                conn.commit()
            except:
                print("not assigned to a contingency zone")
        except:
            print("VMD prior not connected")

        print("session ticket expired,please get a new session ticket from central")
        data = {"central port": "5001", "ticket status":"ticket expired"}
        jsdata = json.dumps(data)
        return jsdata

def ticketValidation(vmd_id):

    answer = mycursor.execute("SELECT curr_timestamp, expiry_time FROM vmd_timestamp where vmd_id=%s",(vmd_id,)) #new table might have to introduce
    answer = mycursor.fetchall()
    for row in answer :
        tcurr_timestamp=row[0]
        exp_time=row[1]

    tims = time.time()
    zcurrent_timestamped = datetime.datetime.fromtimestamp(tims).strftime('%Y-%m-%d %H:%M:%S') 
    zcurrent_timestamped2=datetime.datetime.strptime(zcurrent_timestamped,'%Y-%m-%d %H:%M:%S')

    yc = int(zcurrent_timestamped2.strftime('%Y'))
    mc = int(zcurrent_timestamped2.strftime('%m'))
    dc = int(zcurrent_timestamped2.strftime('%d'))
    hc = int(zcurrent_timestamped2.strftime('%H'))
    minc= int(zcurrent_timestamped2.strftime('%M'))
    sc = int(zcurrent_timestamped2.strftime('%S'))

    zcurr_timestamped = datetime.datetime(yc, mc, dc, hc, minc,sc)

    try:
        ye = int(exp_time.strftime('%Y'))
        print(ye)
        me = int(exp_time.strftime('%m'))
        de = int(exp_time.strftime('%d'))
        he = int(exp_time.strftime('%H'))
        mine= int(exp_time.strftime('%M'))
        se = int(exp_time.strftime('%S'))

        expiry_time = datetime.datetime(ye, me, de, he, mine,se)

        if zcurr_timestamped.time() < expiry_time.time():
            not_expired=1
        else:
            not_expired=0

   # tcurr_timestamp=datetime.datetime.strptime(curr_timestamp,'%Y-%m-%d %H:%M:%S')

        yct = int(tcurr_timestamp.strftime('%Y'))
        mct = int(tcurr_timestamp.strftime('%m'))
        dct = int(tcurr_timestamp.strftime('%d'))
        hct = int(tcurr_timestamp.strftime('%H'))
        minct= int(tcurr_timestamp.strftime('%M'))
        sct = int(tcurr_timestamp.strftime('%S'))

        tcurr_time = datetime.datetime(yct, mct, dct, hct, minct,sct)

    except:
        not_expired=3

    return not_expired

def insideZone(latitude,longitude,vmd_id):

    Ref_zone_lat = (90-zone_lat)*(pi/180)

    Ref_latitude = (90-latitude)*(pi/180)

    Ref_zone_longtitude_input = (zone_longtitude - longitude)*(pi/180)

    Ref_X = cos(Ref_zone_lat)*cos(Ref_latitude)
    Ref_Y = sin(Ref_zone_lat)*sin(Ref_latitude)*cos(Ref_zone_longtitude_input)
    distance = 6371*acos(Ref_X + Ref_Y)
    print(distance)

    if distance > 200:
        within_zone=0
    elif distance<200:
        within_zone=1

    if within_zone == 0:
       
        #-------------remove commentsS
       # mycursor.execute("INSERT into zone_capacity(zone_id , zone_port , zone_name , zone_capacity )values(%s, %s,%s,%s)", (zone_id , zone_port , zone_name , zone_capacity,))
       # conn.commit()
        
        mycursor.execute("DELETE FROM vmd_timestamp where vmd_id=%s", (vmd_id,))
        conn.commit()
        return within_zone
    else:
        return within_zone

        
