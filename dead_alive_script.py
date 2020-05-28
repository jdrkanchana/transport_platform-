from flask import Flask, request,render_template
import mysql.connector
import os
import time
import datetime

from tcping import Ping
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="bat123",
    database="platdb"
)
mycursor = mydb.cursor()
app = Flask(__name__)


@app.route('/')
def index():
    return 'Server Works!'

# Ping(host, port, timeout)
ping = Ping('127.0.0.1', 6001, 60)
try:
    while(1):
        ping.ping() 
        #command = os.system('ping 127.0.0.1 > new.txt') 'ping > new.txt'
        #command = os.system('ping.ping() > new.txt ')
except:
    print("Hello")
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    node_ip ="127.0.0.1:6001"
    mycursor.execute("INSERT into coordinator(node_ip, timestamp) values(%s, %s)", (node_ip, timestamp,))
    mydb.commit()

if __name__ == "__main__":
    app.run()   