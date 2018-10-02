import threading
import signal
import time
import sys
import json
import getopt
import queue as Queue
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
#my imports

import Subscribe as Sub




starting_time = strftime("%H%M%S", localtime()) #hour, minute, second
starting_day = strftime("%d%m%y", localtime())

log_path=os.system('mkdir -p Log')
rasp_id ="A"
logging.basicConfig(filename= 'Log/rasp'+rasp_id+'.log',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

mqtt_data={}

logging.debug("Start smart directions on rasp "+rasp_id)

#basic info for MQTT transmition
broker = "127.0.0.1" #broker as my local address
topic_name =["topic/rasp4/directions/start", "topic/rasp4/directions/stop"]
StartMsg = namedtuple('StartMsg', ['mac_address', 'place_id', 'id', 'timestamp', 'color', 'beacon_flag'])
StopMsg = namedtuple('StopMsg', ['mac_address', 'timestamp'])


if __name__ == "__main__":

    logging.info("*******************************************")
    logging.info("STARTING MAIN")
    logging.info("*******************************************")


    logging.info("*******************************************")
    logging.info("MQTT SUBSCRIPTION")
    logging.info("*******************************************")


    mqtt_data=Sub.subscription(broker, topic_name)
    pp.pprint(mqtt_data)

    logging.info("*******************************************")
    logging.info("LOCAL ENVIRONMENT")
    logging.info("*******************************************")

#### MAIN ####
'''if __name__ == "__main__":
    logging.info("_____________________________")
    logging.info("SM4RT_D1R3CT10Nz v0.3 thread")
    print ("SM4RT_D1R3CT10Nz v0.3 thread", rasp_id)
    logging.info("Starting main...")
  '''






