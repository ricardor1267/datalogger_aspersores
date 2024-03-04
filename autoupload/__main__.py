

#!/usr/bin/python3
import subprocess
import traceback
import requests
import MySQLdb
import time
import json
import sys
import os
import pprint
from datetime import datetime
import json


# Open Config File
f = open('/srv/datalogger_aspersores/config.json')
config = json.load(f)
f.close()


# Identificacion del equipo
MINING_EQUIPO_ID = config["MINING_EQUIPO_ID"]
MINING_FAENA_ID = config["MINING_FAENA_ID"]
TABLE_NAME = config["TABLE_NAME"]

# Local database config
MYSQL_HOSTNAME = 'localhost'
MYSQL_USERNAME = 'root'
MYSQL_PASSWORD = 'claveEye3##'
MYSQL_DATABASE = 'mining_db'

STATION_PUSH_URL = config["URL"]


def log(message):
        print(message)



def checkAndUpload( push_url=STATION_PUSH_URL, mysql_user=MYSQL_USERNAME, mysql_passwd=MYSQL_PASSWORD, mysql_host=MYSQL_HOSTNAME, mysql_db=MYSQL_DATABASE, table_name= TABLE_NAME):

        log("checkAndUpload(%s,%s,%s,%s,%s)" % (push_url, mysql_user, mysql_passwd, mysql_host, mysql_db))

        sql = f"select * from {table_name} where uploaded=0  order by timestamp desc limit 120"
        db = MySQLdb.connect(
                        user=mysql_user,
                        host=mysql_host,
                        passwd=mysql_passwd,
                        db=mysql_db
        )

        log(str(db))
        cursor = db.cursor()
        log(sql)
        cursor.execute(sql)

        res = []
        ids = []
        for row in cursor.fetchall():
                data_dict = dict((cursor.description[i][0], value) for i, value in enumerate(row))
                data_dict.pop("uploaded")
                data_dict["datetime"] = data_dict["datetime"].strftime("%Y/%m/%d %H:%M:%S")
                data_dict["aspersores"] = eval(data_dict["status_aspersores"])
                data_dict.pop("status_aspersores")
                ids.append(data_dict.pop("id"))
                res.append(data_dict)


        db.commit()

        data_sensor= {
                "faena"         : MINING_FAENA_ID,
                "equipo"        : MINING_EQUIPO_ID,
                "data"          : res
                }
        


        pprint.pprint(data_sensor)
        
        if res:
                try:
                                r = requests.post(push_url, json = data_sensor, timeout=15)
                                print(r)
                                print(ids)
                                estado =(r.content).decode("utf-8")
                                log(estado)
                                if estado =='Success':
                                        sql = f"UPDATE {table_name} SET uploaded = %s WHERE id in %s"
                                        val = (1, tuple(ids))
                                        cursor.execute(sql, val)
                                        db.commit()

                except Exception as ex:
                                log('Error request')
                                print(ex)
                                pass
        else:
                log("No hay nueva data")

        cursor.close()
        db.close()



# Main loop
if __name__ == "__main__":
        log("---")
        log("STATION_PUSH_URL: [%s]" % STATION_PUSH_URL)
        log("MYSQL_USERNAME: [%s]" % MYSQL_USERNAME)
        log("MYSQL_PASSWORD: [%s]" % MYSQL_PASSWORD)
        log("MYSQL_HOSTNAME: [%s]" % MYSQL_HOSTNAME)
        log("MYSQL_DATABASE: [%s]" % MYSQL_DATABASE)
        log("---")


        while True:
                try:            
                        checkAndUpload(STATION_PUSH_URL, MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_HOSTNAME, MYSQL_DATABASE, TABLE_NAME)

                except:
                        log('error')
                        e = sys.exc_info()
                        log("dumping traceback for [%s: %s]" % (str(e[0].__name__), str(e[1])))
                        traceback.print_tb(e[2])


                log("sleeping 20 seconds")
                time.sleep(20)
