#!/usr/bin/python3

import logging
import paho.mqtt.client as mqtt
import sys
import os
from collections import namedtuple



#basic info for MQTT transmition

rasp_id ="A"
broker = "127.0.0.1" #broker as my local address
topic_name =["topic/rasp4/directions/start", "topic/rasp4/directions/stop"]
StartMsg = namedtuple('StartMsg', ['mac_address', 'place_id', 'id', 'timestamp', 'color', 'beacon_flag'])
StopMsg = namedtuple('StopMsg', ['mac_address', 'timestamp'])

logging.basicConfig(filename= 'Log/rasp'+rasp_id+'.log',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



def publishing(json_file, broker, topic_name):
    #client.publish(topic_name[0], json_file)
    #
    logging.info("publishing ...")
    os.system("mosquitto_pub -h "+broker+" -m "+json_file+" -t "+ topic_name[0])
    logging.info("The info of the beacon are in : "+ json_file)



