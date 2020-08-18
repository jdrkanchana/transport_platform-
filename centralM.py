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
status="alive"
node_ip ="127.0.0.1:5001"
 
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

        if vmdID is none:
            return "Please enter VMD ID"

        return "Please enter VMD ID"
    try:
        username=input['username']

    except:
        if username is none:
            return "Please enter username"

        return "Please enter username"
    try:
        encrypted_password=input['encrypted_password']

    except:
        if encrypted_password is none:
            return "Please enter encrypted_password"
        return "Please enter encrypted password"
    try:
        driver_id=input['driver_id']

    except:
        if driver_id is none:
            return "Please enter driver id"
        return "Please enter driver license no"
    try:
        latitude=input['latitude'] 

    except:
        if latitude is none:
            return "Please enter latitude"
        return "Please enter latitude"
    try:
        longitude=input['longitude']

    except:
        if longitude is none:
            return "Please enter encrypted_password"
        return "Please enter longitude"
    print("Master central")
    tin = time.time()
    mtimestamp = datetime.datetime.fromtimestamp(tin).strftime('%Y-%m-%d %H:%M:%S')
    mycursor.execute("INSERT into coordinator_alive(node_ip, timestamp,status) values(%s, %s, %s)", (node_ip, mtimestamp,status))
    conn.commit()

    a=1
    b=2
    #check security module
    issueTic=issueTicket(vmdID)
    
    
    dk=issueTic
    authentication=authServer(vmdID, username, encrypted_password,driver_id,dk) 
    if authentication ==100:
        return {"status":"driver not permitted to drive this vehicle"}
    if authentication ==150:
        return {"status":"re enter password"}
    #check is zone alive
    zones_alive=zoneAlive(a)
    #check the local zone
    local_zone=findLocalZone(latitude,longitude)   
    
    #check the zone capacity
    zone_capacity=zoneCapacity(b)

    result1 = mycursor.execute("SELECT zone_id,zone_port,zone_name,zone_status FROM zone_alive")
    result1 = mycursor.fetchall()

    for row in result1 :
        zone_id=row[0]
        
        try:
            if local_zone ==1 and zone_id == 1:
                zone_aloc=1
                
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
    
    sid=mycursor.fetchall()
    for row in sid:
        zone_capacity=row[0]
        
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
    try:
        zone_port
        
    except:
        
        contingency_zone=contingency(b)
        ts = time.time()
        conti_timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        mycursor.execute("INSERT into vmdContingencyZone(vmd_id, conti_timestamp, zone_port) values(%s, %s,%s)", (vmdID,ccurrent_timestamped , contingency_zone,))
        conn.commit()

        mycursor.execute("INSERT into vmd_zone_allocation(vmd_id, zone_alloc_timestamp, zone_port) values(%s, %s,%s)", (vmdID, ccurrent_timestamped, contingency_zone,))
        conn.commit()
        
        if(contingency_zone==6001):
            return {"zone port":"6001"}
        if(contingency_zone==6002):
            return {"zone port":"6002"}
        if(contingency_zone==6003):
            return {"zone port":"6003"}
        if(contingency_zone==6004):
            return {"zone port":"6004"}

def authServer(vmdID, username, encrypted_password,driver_id,dk):
    print(driver_id)
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
    except:
        return 150
    if username==usn:
        credential=1
    else:
        return 150
   # try:
   #     driver_vehicle_category
   # except:
   #     return 0
   
    if driver_vehicle_category==v_category:
        vehicle_can_drive=1
    else:
        return 100

    result = mycursor.execute("SELECT curr_timestamp,expiry_time FROM vmd_timestamp where vmd_id=%s",(vmdID,))
    result = mycursor.fetchall()
    for row in result :
        ticexp_time=row[0]

    tims = time.time()
    ccurrent_timestamped = datetime.datetime.fromtimestamp(tims).strftime('%Y-%m-%d %H:%M:%S') 
    ccurrent_timestamped2=datetime.datetime.strptime(ccurrent_timestamped,'%Y-%m-%d %H:%M:%S')

    yc = int(ccurrent_timestamped2.strftime('%Y'))
    mc = int(ccurrent_timestamped2.strftime('%m'))
    dc = int(ccurrent_timestamped2.strftime('%d'))
    hc = int(ccurrent_timestamped2.strftime('%H'))
    minc= int(ccurrent_timestamped2.strftime('%M'))
    sc = int(ccurrent_timestamped2.strftime('%S'))

    ccurr_timestamped = datetime.datetime(yc, mc, dc, hc, minc,sc)
    try:
        yz = int(ticexp_time.strftime('%Y'))
        mz = int(ticexp_time.strftime('%m'))
        dz = int(ticexp_time.strftime('%d'))
        hz = int(ticexp_time.strftime('%H'))
        minz= int(ticexp_time.strftime('%M'))
        sz = int(ticexp_time.strftime('%S'))

        ticexpiry_time = datetime.datetime(yz, mz, dz, hz, minz,sz)

        if ccurr_timestamped.time() > ticexpiry_time.time():
            new=1
        else:
            new=0
    except:
        new=0
    try:
        ticexp_time
    except:
        new=1

    if dk==1 or new==1:
        needTicket=1
    else:
        needTicket=0
    
    if credential==1 and vehicle_can_drive==1:
        authe=1
        
    else:
        authe=0

    if authe==1 and needTicket==1:
        
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        curr_timestamp=timestamp
        #curr_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S') 
        

        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        hour = time.strftime("%H", t)
        
        t_hours_from_now = datetime.datetime.now() + datetime.timedelta(hours=3)
        expiry_time=t_hours_from_now
        exp_time=t_hours_from_now.isoformat()
        
        ext=t_hours_from_now.replace(microsecond=0)
        #expiry_timestamp = t_hours_from_now.strftime('%Y-%m-%d %H:%M:%S') 
        

        curr_time=datetime.datetime.now().isoformat()
        


        mycursor.execute("INSERT into vmd_timestamp(vmd_id, curr_timestamp, expiry_time) values(%s, %s,%s)", (vmdID, curr_timestamp, expiry_time,))
        conn.commit()

        mycursor.execute("INSERT into vmd_timestamp_log(vmd_id, curr_timestamp, expiry_time) values(%s, %s,%s)", (vmdID, curr_timestamp, expiry_time,))
        conn.commit()
      
        return "connected"
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
    
    result = mycursor.execute("SELECT zone_id FROM zone_dead")
    result = mycursor.fetchall()
    for row in result :
        zone_id=row[0]
        
        print(zone_id)
    mycursor.execute("DELETE FROM zone_alive where zone_id=%s", (zone_id,))
    conn.commit()
    return "zones alive"

def zoneCapacity(b):

    zone_maxlimit=3001
    mycursor.execute("DELETE FROM zone_available where zone_capacity>=%s", (zone_maxlimit,))
    conn.commit()
  
    return "zones free capacity"

def contingency(b):
    
    yid=mycursor.execute("SELECT MIN(zone_capacity) AS minimum FROM zone_available")
    yid =mycursor.fetchall()
    for row in yid :
        min_zone_capacity=row[0]
        
    ans=mycursor.execute("SELECT zone_port FROM zone_available where zone_capacity=%s", (min_zone_capacity,))
    ans =mycursor.fetchall()
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
        

    try:

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
    except:
        
        return "9"