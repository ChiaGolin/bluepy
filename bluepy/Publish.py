#!/usr/bin/python3

import logging
import paho.mqtt.client as mqtt
import sys
import os
from collections import namedtuple
from  subprocess import call



#basic info for MQTT transmition

rasp_id ="A"
#broker = "127.0.0.1" #broker as my local address
broker = "10.79.1.176"
#topic_name =["topic/rasp4/directions/start", "topic/rasp4/directions/stop"]
StartMsg = namedtuple('StartMsg', ['mac_address', 'place_id', 'id', 'timestamp', 'color', 'beacon_flag'])
StopMsg = namedtuple('StopMsg', ['mac_address', 'timestamp'])

logging.basicConfig(filename= 'Log/rasp'+rasp_id+'.log',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



def publishing_start(json_file, broker, topic_name):
    #client.publish(topic_name[0], json_file)
    #
    #client= mqtt.Client()
    logging.info("publishing ...")
    #client.publish("topic", payload="ciao", qos=2, retain=False)
    print(json_file)
    call(["mosquitto_pub", "-h", broker, "-t", topic_name, "-m", json_file ])
    #os.system("mosquitto_pub -h "+broker+" -m "+json_file+" -t "+ topic_name)
    logging.info("The info of the beacon are in : "+ json_file)


def publishing_stop(broker, topic_name, id):

    os.system("mosquitto_pub -h " + broker + " -m "+id+".json  -t " + topic_name)


#publishing_start("ndns", 213123, "bcdnc")



