
import threading
import signal
import time
import sys
import json
import getopt
#import queue as Queue
import subprocess
import logging
import os
import paho.mqtt.client as mqtt
import pathlib
import xml.etree.ElementTree as ET
import pprint as pp
from collections import namedtuple
from datetime import datetime
from time import strftime, localtime
import pprint as pp
from threading import *
from multiprocessing import Process, Queue
from multiprocessing.pool import ThreadPool
import _thread

#my imports

import Subscribe as Sub
import Scan
import blescan2 as ble

BUF_SIZE = 10


starting_time = strftime("%H%M%S", localtime()) #hour, minute, second
starting_day = strftime("%d%m%y", localtime())

log_path=os.system('mkdir -p Log')
rasp_id ="A"
logging.basicConfig(filename= 'Log/rasp'+rasp_id+'.log',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

global mqtt_Data
mqtt_Data={}


logging.debug("Start smart directions on rasp "+rasp_id)

#basic info for MQTT transmition
broker = "127.0.0.1" #broker as my local address
topic_name =["topic/rasp4/directions/start", "topic/rasp4/directions/stop"]
StartMsg = namedtuple('StartMsg', ['mac_address', 'place_id', 'id', 'timestamp', 'color', 'beacon_flag'])
StopMsg = namedtuple('StopMsg', ['mac_address', 'timestamp'])

MAcList=[]
def kill():
    os.system("pkill -f Main.p")

def scanning_list(MQTT_DATA, ble_list):
    #print("sono nella scanning list")
    for i in range(0, len(MQTT_DATA["mac"])):
        MAcList.append(MQTT_DATA["mac"][i])
    rssi=-100

    #rendilo continuo fino all'arrivo o allo scadere del timer
    Scan.read_dict(MAcList, rssi, MQTT_DATA["id"], ble_list)

def timer_scan(MQTT_DATA, TIMER):
    timer = Timer(TIMER, kill)
    timer.start()
    if True:
        scanning_list(MQTT_DATA)

def single_process(MQTT_DATA):
    print("single process")
    print(MQTT_DATA)

    t1=threading.Thread(target=Sub.subscription, args=(broker, topic_name[1]))
    t2 = threading.Thread(target=timer_scan, args=(MQTT_DATA, 360.0))

    t1.start()
    t2.start()







if __name__ == "__main__":

    #thread_queue=Queue.Queue(BUF_SIZE)
    threads=[]
    array_dict=[]
    size=0
    bl_list={}
    prov={}
    open("Thread.txt", 'w').close()

  #  mqtt_Data = {}
#
    logging.info("*******************************************")
    logging.info("STARTING MAIN")
    logging.info("*******************************************")


    logging.info("*******************************************")
    logging.info("MQTT SUBSCRIPTION")
    logging.info("*******************************************")


    # do some other stuff in the main process
    mqttStart_q = Queue

    t_mqtt = Sub.subscribing_thread(topic_name[0])
    t_mqtt.setDaemon(True)
    t_mqtt.start()
        #global mqtt_Data
    while True:

        #print("INIZIO WHILE")
        ble_list=ble.ScanScan()

        #print("SUPERATO IL THREAD")
        time.sleep(5)



        if os.path.getsize("Thread.txt") > 0:
            #print(size)
             #print(os.path.getsize("Thread.txt"))

            with open("Thread.txt", "r") as f:


                while True:
                    line = f.readline()
                    lines=(line.rstrip("\n"))
                    if lines not in threads:
                        threads.append(lines)
                    # check if line is not empty
                    if not line:
                        threads.remove("")
                        size=os.path.getsize("Thread.txt")
                        break

        for i in range (0, len(threads)):
            with open(threads[i]) as f:
                prov=json.load(f)
                array_dict.append(prov)

        for i in range (0, len(array_dict)):
            if array_dict[i]['id']+".json"==threads[i]:
                scanning_list(array_dict[i], ble_list)


        #print(threads)
        threads=[]
        array_dict=[]









   #logging.in("LOCAL ENVIRONMENT")
    #logging.info("*******************************************")






        #mqtt_Data = Sub.subscription(broker, topic_name[0])
        #t=threading.Thread(target=Sub.subscription, args=(broker, topic_name[0]))
        #t.setDaemon(True)

        #t.start()
        #t.join()





#### MAIN ####
'''if __name__ == "__main__":
    logging.info("_____________________________")
    logging.info("SM4RT_D1R3CT10Nz v0.3 thread")
    print ("SM4RT_D1R3CT10Nz v0.3 thread", rasp_id)
    logging.info("Starting main...")
  '''
