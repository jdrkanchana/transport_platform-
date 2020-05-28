from flask import Flask, request
import mysql.connector
import math
import requests
import time
import datetime
from datetime import timedelta
import math
from math import cos, pi,sin,acos 
from time import sleep
from cryptography.fernet import Fernet
from Crypto.Cipher import AES
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

@app.route('/central', methods=['POST'])
def central():

    input = request.get_json()
    print(input)
    try:
        vmdID=input['vmdID']
    except:
        return "Please enter VMD ID"
    try:
        username=input['username']
    except:
        return "Please enter username"
    try:
        encrypted_password=input['encrypted_password']
    except:
        return "Please enter encrypted password"
    try:
        driver_id=input['driver_id']
    except:
        return "Please enter driver license no"
    try:
        latitude=input['latitude'] 
    except:
        return "Please enter latitude"
    try:
        longitude=input['longitude']
    except:
        return "Please enter longitude"

    a=1
    b=2
    #check security module
    issueTic=issueTicket(vmdID)
    print(issueTic)
    dk=issueTic
    authentication=authServer(vmdID, username, encrypted_password,driver_id,dk) 
    #check is zone alive
    zones_alive=zoneAlive(a)
    #check the local zone
    local_zone=findLocalZone(latitude,longitude)   
    print(local_zone)
    #check the zone capacity
    zone_capacity=zoneCapacity(b)

    result1 = mycursor.execute("SELECT zone_id,zone_port,zone_name,zone_status FROM zone_alive")
    result1 = mycursor.fetchall()

    for row in result1 :
        zone_id=row[0]
        print(zone_id)
        try:
            if local_zone ==1 and zone_id == 1:
                zone_aloc=1
                print("funny")
            elif local_zone ==2 and zone_id == 2:
                zone_aloc=2
            elif local_zone ==3 and zone_id == 3:
                zone_aloc=3
            elif local_zone ==4 and zone_id == 4:
                zone_aloc=4
        except NameError:
            return "No zone allocated"

    timez = time.time()
    ccurrent_timestamped = datetime.datetime.fromtimestamp(timez).strftime('%Y-%m-%d %H:%M:%S') 

    sid=mycursor.execute("SELECT zone_capacity FROM zone_available where zone_id=%s",(zone_aloc,))
    print("hate")
    sid=mycursor.fetchall()
    for row in sid:
        zone_capacity=row[0]
        print(zone_capacity)
        if zone_capacity<3000:
            answ = mycursor.execute("SELECT zone_port FROM zone_available where zone_id=%s",(zone_aloc,))
            answ = mycursor.fetchall()

            for row in answ :
                zone_port=row[0]

            if zone_port==6001:
                mycursor.execute("INSERT into vmdLocalZone(vmd_id, local_timestamp, zone_port) values(%s, %s,%s)", (vmdID, ccurrent_timestamped, zone_port,))
                conn.commit()
                mycursor.execute("INSERT into vmd_zone_allocation(vmd_id, zone_alloc_timestamp, zone_port) values(%s, %s,%s)", (vmdID, ccurrent_timestamped, zone_port,))
                conn.commit()
                return {"zone port":"6001"}

            elif zone_port==6002:
                mycursor.execute("INSERT into vmdLocalZone(vmd_id, local_timestamp, zone_port) values(%s, %s,%s)", (vmdID, ccurrent_timestamped, zone_port,))
                conn.commit()
                mycursor.execute("INSERT into vmd_zone_allocation(vmd_id, zone_alloc_timestamp, zone_port) values(%s, %s,%s)", (vmdID, ccurrent_timestamped, zone_port,))
                conn.commit()
                return {"zone port":"6002"}

            elif zone_port==6003:
                mycursor.execute("INSERT into vmdLocalZone(vmd_id, local_timestamp, zone_port) values(%s, %s,%s)", (vmdID, ccurrent_timestamped, zone_port,))
                conn.commit()
                mycursor.execute("INSERT into vmd_zone_allocation(vmd_id, zone_alloc_timestamp, zone_port) values(%s, %s,%s)", (vmdID, ccurrent_timestamped, zone_port,))
                conn.commit()
                return {"zone port":"6003"}

            elif zone_port==6004:
                mycursor.execute("INSERT into vmdLocalZone(vmd_id, local_timestamp, zone_port) values(%s, %s,%s)", (vmdID, ccurrent_timestamped, zone_port,))
                conn.commit()
                mycursor.execute("INSERT into vmd_zone_allocation(vmd_id, zone_alloc_timestamp, zone_port) values(%s, %s,%s)", (vmdID, ccurrent_timestamped, zone_port,))
                conn.commit()
                return {"zone port":"6004"}

            jsdata = json.dumps(data)
            return jsdata
        else:
            contingency_zone=contingency(b)
            conti_timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

            mycursor.execute("INSERT into vmdContingencyZone(vmd_id, conti_timestamp, zone_port) values(%s, %s,%s)", (vmdID, conti_timestamp, zone_port,))
            conn.commit()
            return contingency_zone

def authServer(vmdID, username, encrypted_password,driver_id,dk):

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

    try:
        jet = mycursor.execute("SELECT curr_timestamp, expiry_time FROM vmd_timestamp where vmd_id=%s",(vmdID,)) #new table might have to introduce
        jet = mycursor.fetchall()
        for row in answer :
            curr_timestamp=row[0]
        new=0
    except:
        new=1

    if dk==1 or new ==1:
        needTicket=1
    else:
        needTicket=0

    if username==usn and d==1:
        valid=1
    else:
        valid=0

    if valid==1 and needTicket==1:
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

def findLocalZone(latitude,longitude):
    latitude=latitude
    longitude=longitude
    zoneA_lat = 7.513617    #Westen Zone
    zoneA_longtitude = 80.137133

    zoneB_lat = 6.507628    #Southern Zone
    zoneB_longitude = 80.829782

    zoneC_lat = 7.402797    #Central Zone
    zoneC_longitude = 81.418508

    zoneD_lat = 9.021270    #Northern Zone
    zoneD_longitude = 80.587440

        #Longitude ref value calculation
    Ref_zoneA_lat = (90-zoneA_lat)*(pi/180)
    Ref_zoneB_lat = (90-zoneB_lat)*(pi/180)
    Ref_zoneC_lat = (90-zoneC_lat)*(pi/180)
    Ref_zoneD_lat = (90-zoneD_lat)*(pi/180)

        #latitude ref value calculation 
    Ref_latitude = (90-latitude)*(pi/180)

        #lalilude bitween zone and input calcualtion
    Ref_zoneA_longtitude_input = (zoneA_longtitude - longitude)*(pi/180)
    Ref_zoneB_latitude = (zoneB_longitude - longitude)*(pi/180)
    Ref_zoneC_latitude = (zoneC_longitude - longitude)*(pi/180)
    Ref_zoneD_latitude = (zoneD_longitude - longitude)*(pi/180)

        #distace calculation 
    RefA_X = cos(Ref_zoneA_lat)*cos(Ref_latitude)
    RefA_Y = sin(Ref_zoneA_lat)*sin(Ref_latitude)*cos(Ref_zoneA_longtitude_input)
    distanceA = 6371*acos(RefA_X + RefA_Y)

    RefB_X = cos(Ref_zoneB_lat)*cos(Ref_latitude)
    RefB_Y = sin(Ref_zoneB_lat)*sin(Ref_latitude)*cos(Ref_zoneB_latitude)
    distanceB = 6371*acos(RefB_X + RefB_Y)

    RefC_X = cos(Ref_zoneC_lat)*cos(Ref_latitude)
    RefC_Y = sin(Ref_zoneC_lat)*sin(Ref_latitude)*cos(Ref_zoneC_latitude)
    distanceC = 6371*acos(RefC_X + RefC_Y)

    RefD_X = cos(Ref_zoneD_lat)*cos(Ref_latitude)
    RefD_Y = sin(Ref_zoneD_lat)*sin(Ref_latitude)*cos(Ref_zoneD_latitude)
    distanceD = 6371*acos(RefD_X + RefD_Y)

    zone1=0
    zone2=0
    zone3=0
    zone4=0
    count=0

    if distanceA < 100:
        zonez=1
        count=count+1

    elif distanceB < 100:
        zonez=2
        count=count+1

    elif distanceC < 100:
        zonez=3
        count=count+1

    elif distanceD < 130:
        zonez=4
        count=count+1
    else:
        return "No zone"
    if count>1:
        min_dist=min([distanceA, distanceB, distanceC, distanceD])
        if min_dist==distanceA:
            return 1
        elif min_dist==distanceB:
            return 2
        elif min_dist==distanceC:
            return 3
        elif min_dist==distanceD:
            return 4
    elif zonez==1:
        return 1
    elif zonez==2:
        return 2
    elif zonez==3:
        return 3
    elif zonez==4:
        return 4

def zoneAlive(a):
    print("baby")
    result = mycursor.execute("SELECT zone_id FROM zone_dead")
    result = mycursor.fetchall()
    for row in result :
        zone_id=row[0]
        print("in dummy")
        print(zone_id)
    mycursor.execute("DELETE FROM zone_alive where zone_id=%s", (zone_id,))
    conn.commit()
    return "zones alive"

def zoneCapacity(b):

    answer = mycursor.execute("SELECT zone_id,zone_capacity FROM zone_available")
    answer = mycursor.fetchall()
    print("duckling")
    for row in answer :
        zone_id=row[0]
        print("soappy")
        zone_capacity=row[1]
        if zone_capacity >= 3000:
            mycursor.execute("DELETE FROM zone_available where zone_id=%s", (zone_id))
            conn.commit()
    return "zones free capacity"

def contingency(b):

    yid=mycursor.execute("SELECT MIN(zone_capacity) AS minimum FROM zone_available")
    yid = cursor.fetchall()
    for row in yid :
        min_zone_capacity=row[0]
    ans=mycursor.execute("SELECT zone_port FROM zone_available where zone_capacity=%s", (min_zone_capacity,))
    for row in ans :
        zone_port=row[0]
    return zone_port

def issueTicket(vmdID):

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


    answer = mycursor.execute("SELECT curr_timestamp, expiry_time FROM vmd_timestamp where vmd_id=%s",(vmdID,)) #new table might have to introduce
    answer = mycursor.fetchall()
    for row in answer :
        tcurr_timestamp=row[0]
        exp_time=row[1]
    try:
        ye = int(exp_time.strftime('%Y'))
        print(ye)
        me = int(exp_time.strftime('%m'))
        de = int(exp_time.strftime('%d'))
        he = int(exp_time.strftime('%H'))
        mine= int(exp_time.strftime('%M'))
        se = int(exp_time.strftime('%S'))

        expiry_time = datetime.datetime(ye, me, de, he, mine,se)
#-----------ticket expiry---------------------------------
        if zcurr_timestamped.time() > expiry_time.time():
            jdk=1
            mycursor.execute("DELETE FROM vmd_timestamp where vmd_id=%s", (vmdID,))
            conn.commit()
        try:
            mycursor.execute("DELETE FROM vmdLocalZone where vmd_id=%s", (vmdID,))
            conn.commit()
        except:
            mycursor.execute("DELETE FROM vmdContingencyZone where vmd_id=%s", (vmdID,))
            conn.commit()
        
        else:
            jdk=0
    except:
        jdk=0
#------------zone dead-------------------------------------
    result = mycursor.execute("SELECT zone_id,zone_port FROM zone_dead")
    result = mycursor.fetchall()
    for row in result :
        zone_id=row[0]
        zone_port=row[1]
    try:
        answer2 = mycursor.execute("SELECT zone_port FROM vmdLocalZone where vmd_id=%s",(vmdID,)) #new table might have to introduce
        answer2 = mycursor.fetchall()
        for row in answer2 :
            zone_ported=row[0]
    except:
        ans = mycursor.execute("SELECT zone_port FROM vmdContingencyZone where vmd_id=%s",(vmdID,)) #new table might have to introduce
        ans = mycursor.fetchall()
        for row in ans :
            zone_ported=row[0]


    if zone_port==zone_ported:
        dul=1
        try:
            mycursor.execute("DELETE FROM vmdLocalZone where vmd_id=%s", (vmdID,))
            conn.commit()
        except:
            mycursor.execute("DELETE FROM vmdContingencyZone where vmd_id=%s", (vmdID,))
            conn.commit()
    else:
        dul=0

    if jdk==1 or dul==1:
        dk=1
    else:
        dk=0
    return dk