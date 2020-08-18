import math
from math import cos, pi,sin,acos


#=6371*ACOS(COS(RADIANS(90-D14))*COS(RADIANS(90-D15))+SIN(RADIANS(90-D14))*SIN(RADIANS(90-D15))*COS(RADIANS(E14-E15)))/1.609

zoneA_lat = 7.513617 	#Westen Zone
zoneA_longtitude = 80.137133

zoneB_lat = 6.507628	#Southern Zone
zoneB_longitude = 80.829782

zoneC_lat = 7.402797	#Central Zone
zoneC_longitude = 81.418508

zoneD_lat = 9.021270	#Northern Zone
zoneD_longitude = 80.587440


latitude = 6.065779	#input value
longitude = 80.224271


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

print(distanceA)
print(distanceB)
print(distanceC)
print(distanceD)

if distanceA < 100:
	print("vehical located in zone: A")
if distanceB < 100:
	print("vehical located in zone: B")
if distanceC < 100:
	print("vehical located in zone: C")
if distanceD < 130:
	print("vehical located in zone: D")
