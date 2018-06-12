import sys
import os
import MySQLdb
import urllib
import csv
import string
import re
import pandas as pd
import MySQLdb as mdb

from datetime import datetime
from dateutil.relativedelta import relativedelta


#CHECK DATE
date_after_day = datetime.today()+ relativedelta(days=-1)
date  = date_after_day.strftime('%Y-%m-%d')
date2 = date_after_day.strftime('%Y%m%d')
#print(date)

#CONNECTION DATABASE
mydb = MySQLdb.connect(host='10.200.40.28', user='tats', passwd='tats', db='feeds')
cursor = mydb.cursor()


#CLEAN UP TABLE
query_truncate = "truncate table feeds_cars_multi"
cursor.execute(query_truncate)



select_token = "SELECT token FROM feeds_token"
cursor.execute(select_token)
token2 = list(cursor.fetchall())

#QUERY DB TAKE URL
select = "SELECT url FROM feeds_token"
cursor.execute(select)
result_set = list(cursor.fetchall())
#print result_set
for result in result_set:
        urllib.urlretrieve (result[0], "tmp/feeds.csv")
        os.system("awk 'NR != 1' tmp/feeds.csv > tmp/feeds2.csv")
        os.system("sed 's/ USD//' tmp/feeds2.csv > tmp/feeds_clean.csv")
        csv_data = csv.reader(file('tmp/feeds_clean.csv'))
        for row in csv_data:
                try:
                        cursor.execute("INSERT INTO feeds_cars_multi(insert_date, token, vehicle_id, title, description, url, make, model, year, mileagevalue, mileageunit, transmission, fuel_type, body_style, drivetrain, vin, price, address, exterior_color, availability, state_of_vehicle, latitude, longitude, trim, dealer_id, image0url, image0tag0) VALUES(NOW(), token, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", row)
                except:

                        mydb.commit()

print "SANITY CHECKING"

select_sanity = "SELECT count(*) FROM feeds_cars_multi"
cursor.execute(select_sanity)
result_sanity = cursor.fetchone()
count = result_sanity[0]
print count

if count == 0:
        #query_nagios = "UPDATE feeds_check SET nagios = 0 WHERE id = 1"
        cursor.execute("UPDATE feeds_check SET nagios = 0 WHERE id = 1")
        mydb.commit()
        print cursor._last_executed
        print "NON CI SONO I FEED INTO FEEDS_CARS_MULTI"
        sys.exit(0)

else:
        query_truncate = "drop table feeds_cars"
        cursor.execute(query_truncate)
        query_rename = "rename table feeds_cars_multi to feeds_cars"
        cursor.execute(query_rename)
        query_nagios = "UPDATE feeds_check SET nagios = 1 WHERE id = 1"
        cursor.execute(query_nagios)


query_create = "CREATE TABLE `feeds_cars_multi` (   `insert_date` datetime DEFAULT NULL,   `token` varchar(45) DEFAULT NULL,   `vehicle_id` text,   `title` text,   `description` text,   `url` text,   `make` text,   `model` text,   `year` text,   `mileagevalue` int(11) DEFAULT NULL,   `mileageunit` text,   `transmission` text,   `fuel_type` text,   `body_style` text,   `drivetrain` text,   `vin` text,   `price` int(11) DEFAULT NULL,   `address` text,   `exterior_color` text,   `availability` text,   `state_of_vehicle` text,   `latitude` text,   `longitude` text,   `trim` text,   `dealer_id` text,   `image0url` text, `image0tag0` text,  `image1url` text,   `image2url` text,   `image3url` text,   `image4url` text,   `image5url` text,   `image6url` text,   `image7url` text,   `image8url` text,   `image9url` text ) ENGINE=InnoDB DEFAULT CHARSET=latin1;"
cursor.execute(query_create)
cursor.close()
print "NEWS FEED HAS BEEN IMPORTED INTO FEEDS_CARS"

