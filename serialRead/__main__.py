import sys
import json
import socket
import datetime
import traceback
import serial
import pprint
import threading
from serial import Serial, SerialException
from time import time,sleep
import numpy as np
import MySQLdb
import os
from os.path import join
import subprocess
from USBDevnode import USBDevnode
import random

import requests





class serialRead():
        def __init__(self, port_sensor = 3, baudrate=9600, log_id=""):
                self.baudrate = baudrate
                self.timeout = 0.5
                self.log_id = log_id
                self.fake = 0
                self.data_dic = {}
                self.boton_web= 0

             
                with open("/srv/datalogger_aspersores/config.json","r") as archivo:
                        data_conf=json.load(archivo)
                self.MAQUINA= data_conf["MAQUINA"]



                self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
                self.serverAddressPort = ("127.0.0.1", 20001)



                self.url = "http://54.162.236.190:4000/api/app/setmodo"

                # Crea un hilo que ejecuta la función verificar_estado
                hilo_verificacion_web = threading.Thread(target=self.verificar_estado))
                hilo_verificacion_web.start()



                if self.fake:
                    x = threading.Thread(target=self.FakeData)
                    x.start()
                    self.log("Flujometro listener init [%s @ %s bps]" % (self.port, self.baudrate))

                else:
                    self.usb_sensor = USBDevnode(port_sensor)
                    self.port_sensor = self.usb_sensor.getDevnode()
                    if self.port_sensor=="/dev/ttyUSB0":
                    	self.port_asp = "/dev/ttyUSB1"
                    else:
                    	selfport_asp = "/dev/ttyUSB0"
                    #self.port = "/dev/ttyACM0"
                    print("using %s" % self.port_sensor)
                    self.serialRead_sensor = serial.Serial(self.port_sensor, self.baudrate, timeout=self.timeout)
                    self.serialRead_asp = serial.Serial(self.port_asp, self.baudrate, timeout=self.timeout)
                    self.serialRead_sensor.flushInput()
                    self.serialRead_asp.flushInput()
                    self.log("Sensores listener init [%s @ %s bps]" % (self.port_sensor, self.baudrate))
                    self.log("Aspersores listener init [%s @ %s bps]" % (self.port_asp, self.baudrate))
                    x = threading.Thread(target=self.serialReadData)
                    x.start()

 
        def FakeData(self):
            while True:  
                try:
                    fake_data = [
                           [0, 0, 0, 0, 0, 0, 0, 0, 0 , 0, 0, 0],
                           [0, 0, 1, 0, 0, 1, 0, 1, 0 , 0, 1, 0],
                           [1, 1, 1, 1, 1, 1, 1, 1, 1 , 1, 1, 1],
                    ]

                    
                    now = datetime.datetime.now()
                    self.data_dic["status_aspersores"] = str(random.choice(fake_data))
                    self.data_dic["timestamp"] = datetime.datetime.timestamp(now)
                    self.data_dic["datetime"] = now.strftime("%Y-%m-%d %H:%M:%S")

                    self.emit(self.log_id, json.dumps({'id': self.log_id, 'data':self.data_dic}))
                    for clave in self.data_dic:
                            self.log(clave + ":" + str(self.data_dic[clave]))                                     
                    self.data_dic = {}
                    sleep(3)


                except:
                        print("Error")
                        sleep(1)
                        self.traceback()
                                        
        def serialReadData(self):
                # TODO: Agregar lectura de aspersores
                with open("/srv/datalogger_aspersores/serialRead/config.json","r") as archivo:
                        data=json.load(archivo)
                
                while True:  
                        try:
                                with open("/srv/datalogger_aspersores/serialRead/config.json","r") as archivo:
                                        data=json.load(archivo)
                                #line= self.serialRead.readline() # lectura linea
                                #self.log(line)
                                #if line ==b' \r\n': # linea vacia ---> pasar
                                        #pass

                                #receivedString  = line[0:len(line)-2].decode("utf-8")
                                #data_split = receivedString.split(";")
                                #if data_split[0]=='data':
                                        #data_split = data_split[1:]
                                        #for elem in data_split:
                                                #elem_split = elem.split(":")
                                                #self.data_dic[elem_split[0]] = float(elem_split[1])
                                #print(data)
                                if data["modo"]=="manual":
                                        data_aspersores=data["aspersores"]
                                        mensaje="*"
                                        for i in data_aspersores:
                                                mensaje=mensaje+str(i)
                                        mensaje=mensaje+"*\n"
                                        #print(mensaje)
                                        self.serialRead_asp.write(mensaje.encode('utf-8'))
                                        #print(mensaje)
                                        
                                else:
                                        if self.boton_web==0 :
                                                print('')
                                                #COdigo logico con  sensores
                                                #
                                                data_aspersores = [
                                                        [0, 0, 0, 0, 0, 0, 0, 0, 0 , 0, 0, 0]
                                                ]
                                                #
                                                mensaje="*"
                                                for i in data_aspersores:
                                                        mensaje=mensaje+str(i)
                                                mensaje=mensaje+"*\n"
                                                #print(mensaje)
                                                self.serialRead_asp.write(mensaje.encode('utf-8'))
                                                #print(mensaje)
                                        else:
                                                if 

                                now = datetime.datetime.now()
                                self.data_dic["status_aspersores"] = str(data_aspersores)
                                self.data_dic["timestamp"] = datetime.datetime.timestamp(now)
                                self.data_dic["datetime"] = now.strftime("%Y-%m-%d %H:%M:%S")

                                self.emit(self.log_id, json.dumps({'id': self.log_id, 'data':self.data_dic}))
                                self.log(self.data_dic)                                       
                                self.data_dic = {}
                                sleep(3)

                        except:
                                print("Error")
                                sleep(2)
                                self.traceback()


        

        def discoveryPort(self, name, type_usb):
                id_vendor, id_product = self.getIdDevice(name)
                return self.find_tty_usb(id_vendor, id_product, type_usb)


        def emit(self, event, data=None, namespace=None, callback=None):
                bytesToSend = str.encode(data)
                self.UDPClientSocket.sendto(bytesToSend, self.serverAddressPort)
                

        def find_tty_usb(self, idVendor, idProduct, type_usb):

                for dnbase in os.listdir('/sys/bus/usb/devices'):
                        dn = join('/sys/bus/usb/devices', dnbase)
                        if not os.path.exists(join(dn, 'idVendor')):
                                continue
                        idv = open(join(dn, 'idVendor')).read().strip()
                        if idv != idVendor:
                                continue
                        idp = open(join(dn, 'idProduct')).read().strip()
                        if idp != idProduct:
                                continue
                        for subdir in os.listdir(dn):
                                if subdir.startswith(dnbase+':'):
                                        for subsubdir in os.listdir(join(dn, subdir)):
                                                if type_usb=="USB" and subsubdir.startswith('ttyUSB'):
                                                        return join('/dev', subsubdir)                            

                                                elif type_usb== "ACM" and subsubdir.startswith('tty'):
                                                        d = os.listdir(join(dn,subdir,subsubdir))
                                                        print(d)
                                                        return join('/dev', d[0])
                                                #else:
                                                 #       return None


        def getDateTime(self):
                return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


        def getIdDevice(self, name):
                devices = subprocess.check_output('lsusb', shell=True).decode('utf-8').split('\n')
                for device in devices:
                        try:
                                data = device.split(" ")
                                if data[6] == name:
                                        IDs = data[5].split(":")
                                        id_vendor = IDs[0]
                                        id_product = IDs[1]
                                        return id_vendor, id_product
                        except:
                                continue

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


        def verificar_estado(self):
                while True:
                        try:
                        
                        response = requests.get(self.url)

                        
                        if response.status_code == 200:
                                estado = response.json().get("sistema", None)
                                if estado is not None:
                                        self.boton_web=estado
                        else:
                                print(f"Error al obtener el estado. Código de estado: {response.status_code}")

                        except Exception as e:
                        print(f"Error al realizar la solicitud: {str(e)}")

                        
                        time.sleep(5)


                        
serialRead(log_id="ASPERSORES")
