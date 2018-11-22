#!/usr/bin/env python
from __future__ import print_function
import argparse
import binascii
import os
import sys
from bluepy import btle
import pprint as pp
import blescan2 as ble
import logging
import threading
import queue
from collections import namedtuple
import datetime
import xml.etree.ElementTree as ET
import xml_parser

import time

import threading


# my import
import Publish as Pub



rasp_id ="A"
broker = "127.0.0.1"
topic_name =["topic/rasp4/directions/start", "topic/rasp4/directions/stop"]

class timer_Thread(threading.Thread):
    def __init__(self, sec, timer_queue):
        threading.Thread.__init__(self)
        self.sec=sec
        self.timer_queue=timer_queue

    def run(self):
        time.sleep(self.sec)
        self.timer_queue.put("stop")

def open_map(map_path):
    tree = ET.parse(map_path)
    root = tree.getroot()
    return root

class Scan_list(threading.Thread):
    def __init__(self, MAcList, ble_list, place_id, id, color,exit, direction_q, del_direction_q ):
        threading.Thread.__init__(self)
        self.MAcList=MAcList
        self.ble_list=ble_list
        self.place_id=place_id
        self.exit=exit
        self.id=id
        self.color=color
        self.direction_q=direction_q
        self.del_direction_q=del_direction_q

    def run(self):

        print("SCAN")

        #QUEUE
        timer_queue = queue.Queue()

        #VARIABLE
        timer=0 #per sapere se è già partito il timer
        found = 0
        exit=0
        near=0
        final=None


        #ARRAY
        rssi_list=[]


        root = open_map("map.xml")


        TIMER = timer_Thread(360, timer_queue)
        TIMER.setDaemon(True)
        TIMER.start()



        while exit==0:

            direction=None
            #pp.pprint(self.ble_list)
            if len(self.ble_list)>0:
                for i in range(0, len(self.MAcList)):
                    for key, val in self.ble_list.items():
                        if key == self.MAcList[i]:
                            rssi_list.append(val['rssi'])
                            found = 1



            if found == 1:
                found=0
                print(str(rssi_list))
                rssi = ble.RSSI_ave(rssi_list)
                rssi_list=[]


                if float(rssi) < (-80.4):
                    status = "Really far away"

                if float(rssi) < (-70.5) and float(rssi) >= (-80.4):
                    status = "Far away"

                if float(rssi) < (-65) and float(rssi) >= (-70.5):
                    status = "Is coming"

                    direction, final = xml_parser.find_direction(root, self.place_id, rasp_id)


                if float(rssi) < (-54) and float(rssi) >= (-65):
                    status = "Close"

                    direction, final = xml_parser.find_direction(root, self.place_id, rasp_id)


                if float(rssi) >= (-54):
                    status = "Really close"
                    direction, final = xml_parser.find_direction(root, self.place_id, rasp_id)


                if not timer_queue.empty():
                    self.exit.put("stop")
                    exit=1

                elif final==True and float(rssi)>=-67:

                    print("Beacon " + str(self.id) + "\t" + str(rssi) + "\t" + str(status) + "\t" + str(self.place_id) + "\t" + str(direction))

                    return_dict = {"direction": direction,
                                   "color": self.color,
                                   "id": self.id}

                    self.exit.put(return_dict)
                    Pub.publishing_stop(broker, topic_name[1], self.id)
                    exit=1
                    time.sleep(5)

                else:

                    return_dict = {"direction": direction,
                                   "color": self.color,
                                   "id": self.id}

                    print("Beacon " + str(self.id) + "\t" + str(rssi) + "\t" + str(status) + "\t" + str(self.place_id) + "\t" + str(direction))
                    if float(rssi) >= (-70.5) and near==0:
                        near=1

                        print("INVIO NUOVA DIR")
                        self.direction_q.put(return_dict)

                    if float(rssi) < (-70.5) and near==1:
                        #print("Beacon " + str(self.id) + "\t" + str(rssi) + "\t" + str(status) + "\t" + str(self.place_id) )
                        print("CANCELLA DIR")
                        self.del_direction_q.put(return_dict)
                        near=0

                time.sleep(2)



        sys.exit()



















