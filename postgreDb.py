import psycopg2

try: 
 conn = psycopg2.connect(database="platdb", user="postgres", password="bat123", host="localhost")
 print("connected")
except:
 print ("I am unable to connect to the database")
cur =conn.cursor()

#sql = "INSERT INTO vmdCentralScript(latitude, longitude, vmd_id, timestamped) VALUES (%s, %s, %s, %s)

#Doping EMPLOYEE table if already exists.
#cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")

#cur.execute("CREATE TABLE driver (driver_id VARCHAR(20) PRIMARY KEY NOT NULL, driver_name VARCHAR (45) NOT NULL, driver_BOD DATE NOT NULL,driver_vehicle_category VARCHAR (20) NOT NULL, driver_address VARCHAR (200) NOT NULL,driver_tel VARCHAR (45) NOT NULL,driver_blood_group VARCHAR (9) NOT NULL,driver_issueD DATE NOT NULL,driver_expiryD DATE NOT NULL  );")

#cur.execute("CREATE TABLE vehicle (vmd_id serial PRIMARY KEY NOT NULL, v_NumPlate VARCHAR (45) NOT NULL, v_Color VARCHAR(45) NOT NULL ,v_Brand VARCHAR (45) NOT NULL,v_Category VARCHAR (45) NOT NULL);")
#cur.execute("CREATE TABLE CentralScript(vmd_id NUMERIC NOT NULL, latitude DECIMAL NOT NULL, longitude DECIMAL NOT NULL, current_timestamped TIMESTAMP NOT NULL );")

#cur.execute("CREATE TABLE zone_available(zone_id NUMERIC NOT NULL, zone_port NUMERIC NOT NULL, zone_name VARCHAR(20) NOT NULL, zone_capacity NUMERIC NOT NULL );")
#cur.execute("CREATE TABLE zone_capacity(zone_id NUMERIC NOT NULL, zone_port NUMERIC NOT NULL, zone_name VARCHAR(20) NOT NULL, zone_capacity NUMERIC NOT NULL );")
#cur.execute("CREATE TABLE zone_alive(zone_id NUMERIC NOT NULL, zone_port NUMERIC NOT NULL, zone_name VARCHAR(20) NOT NULL, zone_status VARCHAR(40) NOT NULL );")
#cur.execute("CREATE TABLE zone_dead(zone_id NUMERIC NOT NULL, zone_port NUMERIC NOT NULL, zone_name VARCHAR(20) NOT NULL, zone_status VARCHAR(40) NOT NULL );")
#cur.execute("CREATE TABLE vmdContingencyZone(vmd_id NUMERIC NOT NULL,conti_timestamp TIMESTAMP NOT NULL, zone_port NUMERIC NOT NULL );")
#cur.execute("CREATE TABLE vmdLocalZone(vmd_id NUMERIC NOT NULL,local_timestamp TIMESTAMP NOT NULL, zone_port NUMERIC NOT NULL );")
#cur.execute("CREATE TABLE vmd_zone_allocation(vmd_id NUMERIC NOT NULL,zone_alloc_timestamp TIMESTAMP NOT NULL, zone_port NUMERIC NOT NULL );")
#cur.execute("CREATE TABLE vmd_timestamp_log(vmd_id NUMERIC NOT NULL, curr_timestamp TIMESTAMP NOT NULL,expiry_time TIMESTAMP NOT NULL);")
#cur.execute("CREATE TABLE auth (vmd_id serial NOT NULL, username VARCHAR (45) PRIMARY KEY NOT NULL, encrypted_password VARCHAR(200) NOT NULL );")
#cur.execute("CREATE TABLE zoned (vmd_id serial PRIMARY KEY NOT NULL, zoneip INET NOT NULL );")
#cur.execute("CREATE TABLE vmd_timestamp (vmd_id NUMERIC NOT NULL, curr_timestamp TIMESTAMP NOT NULL,expiry_time TIMESTAMP NOT NULL);")

#cur.execute("CREATE TABLE coordinator_alive (node_ip VARCHAR (45) NOT NULL, timestamp TIMESTAMP NOT NULL,status VARCHAR (45) NOT NULL);")
#cur.execute("CREATE TABLE coordinator_dead (node_ip VARCHAR (45) NOT NULL, timestamp TIMESTAMP NOT NULL,status VARCHAR (45) NOT NULL);")

#mycursor.execute("INSERT into vmd_timestamp(vmd_id, current_timestamp, expiry_time) values(%s, %s)", (vmdID, current_timestamp, expiry_time,))

#cur.execute("INSERT into coordinator(node_ip, timestamp) VALUES(%s, %s)", ("127.0.0.1:6001", "2020-05-23 02:52:03.000000",))

#cur.execute("CREATE TABLE employee (e_id serial PRIMARY KEY, age integer, employee_name varchar,ts TIMESTAMP);")
#cur.execute("INSERT INTO customer (age, employee_name) VALUES (%s, %s)",(100, "Polly"))
#cur.execute("INSERT INTO customer (age, employee_name) VALUES (%s, %s)",(30, "Tommy"))

#cur.execute("INSERT INTO driver (driver_id, driver_name , driver_BOD ,driver_vehicle_category, driver_address ,driver_tel ,driver_blood_group ,driver_issueD ,driver_expiryD) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",('B3978409',"A.B.C. Perere", '1997-01-01','A1', 'No 164,2, Waligama, Mathara','770845200','A+','2017-11-06','2025-03-06'))
#cur.execute("INSERT INTO driver (driver_id, driver_name , driver_BOD ,driver_vehicle_category, driver_address ,driver_tel ,driver_blood_group ,driver_issueD ,driver_expiryD) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",('A1893034', "S. Kumara", '1997-01-02','B1','No 22/341, Katubadda, Moratuwa','712345134','AB+','2022-05-09','2023-10-06'))
#cur.execute("INSERT INTO driver (driver_id, driver_name , driver_BOD ,driver_vehicle_category, driver_address ,driver_tel ,driver_blood_group ,driver_issueD ,driver_expiryD) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",('C5567923',"A.P. Peris", '1995-12-06','A1 B1','No 81/31, Kaluthara uthura, Kaluthara','711345100','O-','2015-05-02','2023-10-06'))

#cur.execute("INSERT INTO vehicle (v_NumPlate , v_Color ,v_Brand, v_Category) VALUES ( %s, %s, %s, %s)",('ABC3562','Blue','Isuzu','D1'))
#cur.execute("INSERT INTO vehicle (v_NumPlate , v_Color ,v_Brand, v_Category) VALUES ( %s, %s, %s, %s)",('GA5567','Weight','Toyoto','C1'))
#cur.execute("INSERT INTO vehicle (v_NumPlate , v_Color ,v_Brand, v_Category) VALUES ( %s, %s, %s, %s)",('UG2236','Black','Bajaj','Q'))

#cur.execute("INSERT INTO zone_alive(zone_id , zone_port , zone_name , zone_status ) VALUES (%s, %s, %s, %s)",(1,6001,'zone1','active'))
#cur.execute("INSERT INTO zone_alive(zone_id , zone_port , zone_name , zone_status ) VALUES (%s, %s, %s, %s)",(3,6003,'zone3','active'))
#cur.execute("INSERT INTO zone_alive(zone_id , zone_port , zone_name , zone_status ) VALUES (%s, %s, %s, %s)",(4,6004,'zone4','active'))
#cur.execute("INSERT INTO zone_alive(zone_id , zone_port , zone_name , zone_status ) VALUES (%s, %s, %s, %s)",(2,6002,'zone2','active'))



#cur.execute("INSERT INTO zone_available(zone_id , zone_port , zone_name , zone_capacity ) VALUES (%s, %s, %s, %s)",(3,6003,'zone3',800))

cur.execute("INSERT INTO zone_capacity(zone_id , zone_port , zone_name , zone_capacity ) VALUES (%s, %s, %s, %s)",(1,6001,'zone1',4000))


#cur.execute("INSERT INTO zone_available(zone_id , zone_port , zone_name , zone_capacity ) VALUES (%s, %s, %s, %s)",(2,6002,'zone1',700))
#cur.execute("INSERT INTO zone_available(zone_id , zone_port , zone_name , zone_capacity ) VALUES (%s, %s, %s, %s)",(4,6004,'zone1',200))




#cur.execute("INSERT INTO zone_available(zone_id , zone_port , zone_name , zone_capacity ) VALUES (%s, %s, %s, %s)",(1,6001,'zone1',2600))

#cur.execute("INSERT INTO vmdLocalZone(vmd_id ,local_timestamp, zone_port  ) VALUES (%s, %s, %s)",(1,"2020-05-26 06:10:29",6001))

#cur.execute("INSERT INTO vmd_timestamp(vmd_id , curr_timestamp, expiry_time) VALUES (%s, %s, %s)",(3,"2020-05-28 11:10:29","2020-05-29 01:10:29"))

#zone_port=6001
#cur.execute("DELETE FROM zone_available where zone_port=%s", (zone_port,))

#cur.execute("INSERT INTO zone_dead(zone_id , zone_port , zone_name , zone_status ) VALUES (%s, %s, %s, %s)",(3,6003,'zone3','dead'))
#cur.execute("INSERT INTO auth (username ,encrypted_password) VALUES ( %s, %s)",('DillyD!','gAAAAABewOvHx9zWCt7j3HLZHI6tcZaIoyB4kojIDHkvgeZpv-xiWAzOiOA4HLKx18TFoHgIjLi_-8eOEW3x-z2hY--W7HwUOQ=='))
#cur.execute("INSERT INTO auth (username ,encrypted_password) VALUES ( %s, %s)",('LasithaE!','gAAAAABewOuXtaFZ1nfPu2XCC0HQtf4Ero3flzKY3XSDXOOA-HJbCyJaeCL5337TPDnc5pOqD8pP43dePE7N93jJJAUAZJExLQ=='))
#cur.execute("INSERT INTO auth (username ,encrypted_password) VALUES ( %s, %s)",('IsuruJ!','gAAAAABewOqqF8BOwL8YeykIbpvYPm-q9zuJ5b0Wx7fseIpbMCu8ah-Yne6wL6Bs3jmKlmxKnA7qQdnjwyDXiy6wr1Ra8qi9cQ=='))
#cur.execute("INSERT INTO auth (username ,encrypted_password) VALUES ( %s, %s)",('AruniK!','gAAAAABewOtZ2hYg_Ug3yzZmu7lsSA6THgKryG9kiLW04HuPM9WxMSiRgJJ4ipmY2dI3oB0alyhQp3-JpKb_5WLqNlxyqhUF8Q=='))

#cur.execute("INSERT INTO ipzones (zoneip)  VALUES (%s)",("127.0.0.1:6003",))
#cur.execute("INSERT INTO ipzones (zoneip)  VALUES (%s)",("127.0.0.1:6004",))

#zone_id=1
#cur.execute("DELETE FROM zone_capacity where zone_id=%s", (zone_id,))
#conn.commit()
print("Table created successfully........")

conn.commit()
#Closing the connection
conn.close()
cur.close()



