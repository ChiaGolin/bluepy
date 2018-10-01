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
import pathlib
import xml.etree.ElementTree as ET
import pprint as pp
from collections import namedtuple
from datetime import datetime
from time import strftime, localtime
#my imports
import MQTT_Handler
#import PingHandler
#import ProjectorHandler


starting_time = strftime("%H%M%S", localtime()) #hour, minute, second
starting_day = strftime("%d%m%y", localtime())

log_path=os.system('mkdir -p Log')
rasp_id ="A"
logging.basicConfig(filename= 'Log/rasp'+rasp_id+'.log',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.debug("Start smart directions on rasp "+rasp_id)

broker_address = "127.0.0.1" #broker as my local address
topic_name = "topic/rasp4/directions"

#messages type
#two topics (start, stop)
StartMsg = namedtuple('StartMsg', ['mac_address', 'place_id', 'id', 'timestamp', 'color', 'beacon_flag'])
StopMsg = namedtuple('StopMsg', ['mac_address', 'timestamp'])



























#### MAIN ####
if __name__ == "__main__":
    logging.info("_____________________________")
    logging.info("SM4RT_D1R3CT10Nz v0.3 thread")
    print ("SM4RT_D1R3CT10Nz v0.3 thread", rasp_id)
    logging.info("Starting main...")
    #setup display

    client=paho




