
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

import pprint as pp
from collections import namedtuple
from datetime import datetime
from time import strftime, localtime
import pprint as pp
from threading import *
from multiprocessing import Process, Queue
from multiprocessing.pool import ThreadPool
import _thread
import queue

#my imports

import Subscribe as Sub
import Scan
import blescan2 as ble

BUF_SIZE = 10


starting_time = strftime("%H%M%S", localtime()) #hour, minute, second
starting_day = strftime("%d%m%y", localtime())

log_path=os.system('mkdir -p Log')
rasp_id ="A"
#place_id="0001"

logging.basicConfig(filename= 'Log/rasp'+rasp_id+'.log',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

global mqtt_Data
mqtt_Data={}


logging.debug("Start smart directions on rasp "+rasp_id)

#basic info for MQTT transmition
broker = "127.0.0.1" #broker as my local address
broker = "10.79.1.176"
topic_name =["topic/rasp4/directions/start", "topic/rasp4/directions/stop"]
StartMsg = namedtuple('StartMsg', ['mac_address', 'place_id', 'id', 'timestamp', 'color', 'beacon_flag'])
StopMsg = namedtuple('StopMsg', ['mac_address', 'timestamp'])

MAcList=[]
def kill():
    os.system("pkill -f Main.p")

def scanning_list(MQTT_DATA, ble_list):

    MAcList=[]
    for i in range(0, len(MQTT_DATA["mac"])):
        MAcList.append(MQTT_DATA["mac"][i])
        place_id=MQTT_DATA["place_id"]


    rssi=-100

    #rendilo continuo fino all'arrivo o allo scadere del timer
    Scan.read_dict(MAcList, rssi, MQTT_DATA["id"], ble_list,place_id )

def timer_scan(MQTT_DATA, TIMER):
    timer = Timer(TIMER, kill)
    timer.start()
    if True:
        scanning_list(MQTT_DATA)

def single_process(MQTT_DATA):

    t1=threading.Thread(target=Sub.subscription, args=(broker, topic_name[1]))
    t2 = threading.Thread(target=timer_scan, args=(MQTT_DATA, 360.0))

    t1.start()
    t2.start()


check=0


if __name__ == "__main__":


    threads="None"
    THREADS=[]
    array_dict=[]
    size=0
    bl_list={}
    id_list=[]
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
    sub_q=queue.Queue(BUF_SIZE)
    del_q = queue.Queue(BUF_SIZE)
    data_queue = queue.Queue(BUF_SIZE)




    t_mqtt = Sub.subscribing_thread(topic_name, sub_q, del_q)
    t_mqtt.setDaemon(True)
    t_mqtt.start()



    while True:
        #canc=0


        #pp.pprint(ble_list)



        if not sub_q.empty():

            threads=sub_q.get()
            print("thread: "+threads)

            with open(threads) as f:
                try:
                    prov=json.load(f)
                    if prov["id"] not in id_list:
                        array_dict.append(prov)
                        print("SONO ENTRATO")
                        print(array_dict)
                        id_list.append(prov["id"])
                        print(id_list)

                except:
                    print("Malformed json")



        #print(str(array_dict))
        if len(array_dict)>0:
            print("why")
            ble_list = ble.ScanScan()
            #time.sleep(1)

            #print(len(array_dict))
            for i in range (0, len(array_dict)):
                th=threading.Thread(target=scanning_list, args=(array_dict[i], ble_list))
                THREADS.append(th)
                th.start()
                th.join()



        if not del_q.empty():
            del_value=del_q.get()
            i=0
            canc=0
            while canc==0 and len(array_dict)>0 and i<len(array_dict):
                print("i= "+str(i))
                if array_dict[i]['id']+".json"==del_value:

                    del array_dict[i]
                    canc=1
                i=i+1


        threads=[]







