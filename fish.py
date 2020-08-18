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

@app.route('/zone', methods=['POST'])
def zone():

    input = request.get_json()
    print(input)
    return {"status":"connected"}