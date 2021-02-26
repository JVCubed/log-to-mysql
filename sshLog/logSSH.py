#!/usr/bin/python

# imports
# https://pypi.org/project/tailhead/
import tailhead
# https://pypi.org/project/mysql-connector-python/
# https://www.w3schools.com/python/python_mysql_insert.asp
import mysql.connector
import time
from datetime import datetime
from geolite2 import geolite2

# Variables
dstCountry = ""
DBuser = ""
DBpass = ""
DBip = ""

# set database information
mydb = mysql.connector.connect(
  host=DBip,
  port="3306",
  user=DBuser,
  password=DBpass,
  database="log"
)

mycursor = mydb.cursor()

reader = geolite2.reader()

user_unknown = ": Failed password for invalid user "
user_known = ": Failed password for "

def SQLadd(datetime, user, ip, country):
  sql = "INSERT INTO ssh (time, username, srcIp, srcCountry, dstServer, dstCountry) VALUES (STR_TO_DATE(%(date)s,'%Y %b %d %k:%i:%s'), %(name)s, %(srcIpAddress)s, %(srcCountry)s, %(dstServer)s, %(dstCountry)s)"
  mycursor.execute(sql, { 'date': datetime, 'name': user, 'srcIpAddress': ip, 'srcCountry': country, 'dstServer': DBuser, 'dstCountry': dstCountry})

  mydb.commit()
  #print(datetime, user, ip, country)

for line in tailhead.follow_path('/var/log/auth.log'):
    if line is not None:
        try:
            if user_unknown in line or user_known in line:
                list = line.split()
                date = str(datetime.now().year) + " " + " ".join(list[:3])
                var_user = user_unknown if user_unknown in line else user_known
                user = line.split(var_user,1)[1].rsplit(" from ")[0]
                ip =list[-4]
                match = reader.get(ip)
                try:
                    country = match['country']['iso_code']
                except:
                    country = ""
                    pass
                SQLadd(date, user, ip, country)
        except ValueError as e:
            print(f'Error: {e}')
            continue
    else:
        time.sleep(1)