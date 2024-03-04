import sys
import time
import json
import socket
import MySQLdb
import datetime
import traceback
import threading
from datetime import datetime
from time import time, sleep

   



class server():
        def __init__(self, log_id="Server"):
            self.log_id = log_id
            self.MYSQL_HOSTNAME = 'localhost'
            self.MYSQL_USERNAME = 'root'
            self.MYSQL_PASSWORD = 'claveEye3##'
            self.MYSQL_DATABASE = 'mining_db'


            self.localIP = "127.0.0.1"
            self.localPort = 20001
            self.bufferSize = 1024
            self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
            self.UDPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.UDPServerSocket.bind((self.localIP, self.localPort))

            self.last_hour = 0

            x = threading.Thread(target=self.readDataClient)
            x.start()
    

        def readDataClient(self):
                self.log("Server init listening [%s port %s]" % (self.localIP, self.localPort))
                while True:
                        try:

                                bytesAddressPair = self.UDPServerSocket.recvfrom(self.bufferSize)
                                message = bytesAddressPair[0].decode('utf-8')
                                msg =  json.loads(message)
                                self.log(msg)
             
                                header = msg['id'] 
                                if header == "ASPERSORES":
                                        self.process_data(data=msg["data"], table_name="aspersores_data")
                                        #self.insertData(msg["data"], "ASPERSORES")

                                sleep(0.1)

                        except:
                                self.traceback()
                                sleep(0.5)
    
        def get_last_data(self, table_name):
                last_status = None

                try:
                    sql = f"select * from {table_name} where uploaded=0 order by timestamp desc limit 1"
                    db = MySQLdb.connect(
                                    user= self.MYSQL_USERNAME,
                                    host= self.MYSQL_HOSTNAME,
                                    passwd= self.MYSQL_PASSWORD,
                                    db= self.MYSQL_DATABASE
                    )

                    cursor = db.cursor()
                    self.log(sql)
                    cursor.execute(sql)
                    last_data = cursor.fetchone()
                    self.log(f"Last data: {last_data}")

                    if last_data:
                        last_status = last_data[1]
                except:
                        self.traceback()
                        sleep(0.5)
                
                return last_status

        def process_data(self, data, table_name):
                # insert_data = None
                self.log(f"Process Data")
                try:
                        # Check last data
                        last_data = self.get_last_data(table_name=table_name)

                        # Check hora actual
                        now = datetime.now()
                        current_hour= now.hour

                        # Check ultima hora
                        if current_hour!= self.last_hour:
                                self.log("Ha pasado 1 hora, se debe guardar la data")
                                self.last_hour = current_hour
                                self.insertData(data, table_name)

                        # Check si nuevo dato es igual al anterior
                        elif last_data == data["status_aspersores"]:
                                self.log("No hay cambios de status en los aspersores")
                        else:
                                self.insertData(data, table_name)
                                
                except:
                        self.traceback()
                        sleep(0.5)


        def insertData(self, data_dict, name_table):
                try:
                        self.log(f"Insertando Data: {data_dict}")
                        
                        placeholder = ", ".join(["%s"] * len(data_dict))
                        stmt = "insert into `{table}` ({columns}) values ({values});".format(table=name_table, columns=",".join(data_dict.keys()), values=placeholder)

                        conn = MySQLdb.connect(self.MYSQL_HOSTNAME, self.MYSQL_USERNAME, self.MYSQL_PASSWORD, self.MYSQL_DATABASE)
                        cursor = conn.cursor()
                        cursor.execute(stmt, list(data_dict.values()))

                        conn.commit()
                        cursor.close()
                        conn.close()


                except:
                        self.traceback()  


        def getDateTime(self):
                return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


        def emit(self, event, data=None, namespace=None, callback=None):
                bytesToSend = str.encode(data)
                self.UDPClientSocket.sendto(bytesToSend, self.serverAddressPort)
                #self.log("Trying to emit(%s,%s) but there is no socket.io server" % (str(event), str(data)))

        def log(self,message):
                dt = self.getDateTime()
                print("[%s] %s | %s" % (self.log_id, dt, message))
                with open ("/log.txt", "a") as myfile:
                        myfile.write("[%s] %s | %s\n" % (self.log_id, dt, message))


        def traceback(self):
                try:
                        e = sys.exc_info()
                        self.log("dumping traceback for [%s: %s]" % (str(e[0].__name__), str(e[1])))
                        traceback.print_tb(e[2])
                except:
                        foo = "bar"

s = server()

