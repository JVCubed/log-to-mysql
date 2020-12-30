#!/usr/bin/python

# imports
#  https://pypi.org/project/tailer/
import tailer
#  https://pypi.org/project/mysql-connector-python/
import mysql.connector
# Install geolite2 with
#  pip3 install maxminddb 
#  pip3 install maxminddb-geolite2
#   according to: https://stackoverflow.com/questions/32575666/python-geoip-does-not-work-on-python3-4
from geolite2 import geolite2
from datetime import datetime


# set database information
#  https://www.w3schools.com/python/python_mysql_insert.asp
#  the database and tables have to be created before running this script. below the 'CREATE TABLE' statement I used in this case:

#CREATE TABLE ssh_attempt.log (
#  id INT AUTO_INCREMENT,
#  time DATETIME NOT NULL,
#  username VARCHAR(100),
#  srcIp VARCHAR(15),
#  country VARCHAR(2),
#  PRIMARY KEY(id)
#);

#  make sure your user has the correct permissions on the database.
#  set database information
mydb = mysql.connector.connect(
  host="localhost",
  user="python",
  password="q3#ZJ2cnSP;9W$-[TAFH+mVrfK6%d/_TSwV4pXW@%278^b5xEq}8M~#W$n.C4/U9!JAd;?rGLPqtE(tbJSd$u%-Gmmq*zvvcoa{-",
  database="ssh_attempt"
)
mycursor = mydb.cursor()

# set reader for GeoIP
reader = geolite2.reader()

# Define strings to check
userUnknown = ": Failed password for invalid user"
userKnown = ": Failed password for"

# Function to add info to database
def SQLadd(datetime, user, ip, country):
  sql = "INSERT INTO log (time, username, srcIp, country) VALUES (STR_TO_DATE(%(date)s,'%Y %b %d %k:%i:%s'), %(name)s, %(ipAddress)s, %(country)s)"
  mycursor.execute(sql, { 'date': datetime, 'name': user, 'ipAddress': ip, 'country': country})

  mydb.commit()
  print(datetime, user, ip, country)

# Follow the file as it grows
for line in tailer.follow(open('/var/log/auth.log')):
  #
  if userUnknown in line:
    list = line.split()
    currentYear = str(datetime.now().year)
    date = currentYear + " " + " ".join(list[0:3])
    user = list[10]

    ip = list[12]
    match = reader.get(ip)
    country = match['country']['iso_code']

    SQLadd(date, user, ip, country)

  elif userKnown in line:
    list = line.split()

    currentYear = str(datetime.now().year)
    date = currentYear + " " + " ".join(list[0:3])
    user = list[8]

    ip = list[10]
    match = reader.get(ip)
    country = match['country']['iso_code']

    SQLadd(date, user, ip, country)
