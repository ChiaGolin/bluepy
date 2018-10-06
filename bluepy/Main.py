
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

def scanning_list(MQTT_DATA):
    #print("scanning")
    #print(MQTT_DATA)
    print(MQTT_DATA['id'])
    for i in range(0, len(MQTT_DATA["mac"])):
        MAcList.append(MQTT_DATA["mac"][i])
    rssi=-100

    #rendilo continuo fino all'arrivo o allo scadere del timer
    Scan.read_dict(MAcList, rssi, MQTT_DATA["id"])

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
    thread=[]
    ID_list=[]
    MQTT_DATA={}
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

        #global mqtt_Data
    while True:
        mqtt_Data = Sub.subscription(broker, topic_name[0])
        #t=threading.Thread(target=Sub.subscription, args=(broker, topic_name[0], mqtt_Data))
        #t.setDaemon(True)
        #t.start()
        print("prima join")
        #t.join()
        print(",saòdx,as")

        #mqtt_Data=Sub.subscription(broker, topic_name[0])
        print("**********************************************")
        print(mqtt_Data)
        print("**********************************************")
        MQTT_DATA=mqtt_Data
        print("+++++++++++++++++++++++++++++++++++++++++++++++")
        print(MQTT_DATA)
        print("+++++++++++++++++++++++++++++++++++++++++++++++")
        if len(MQTT_DATA)>0:
            if MQTT_DATA["id"] not in ID_list:
                print("sono nel maledettissimo if")
                print(MQTT_DATA)
                t1=threading.Thread(target=single_process, args=(dict(MQTT_DATA),))
                t1.start()
        mqtt_Data.clear()



   #logging.in("LOCAL ENVIRONMENT")
    #logging.info("*******************************************")











#### MAIN ####
'''if __name__ == "__main__":
    logging.info("_____________________________")
    logging.info("SM4RT_D1R3CT10Nz v0.3 thread")
    print ("SM4RT_D1R3CT10Nz v0.3 thread", rasp_id)
    logging.info("Starting main...")
  '''






