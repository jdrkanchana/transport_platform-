from flask import Flask, request,render_template
import mysql.connector
import os
import time
import datetime

from tcping import Ping
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

ping = Ping('127.0.0.1', 5001, 60)
try:
    while(1):
        ping.ping() 
except:
    print("dead")
    status="dead"
    ts = time.time()
    mtimestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    node_ip ="127.0.0.1:5001"

    mycursor.execute("INSERT into coordinator_dead(node_ip, timestamp,status) values(%s, %s, %s)", (node_ip, mtimestamp,status))
    conn.commit()

    print("Electing new master as the central")

