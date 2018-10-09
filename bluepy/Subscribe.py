import logging
import paho.mqtt.client as mqtt
import sys
import json
import os
from collections import namedtuple
import pprint as pp
import time
from threading import *

import threading
import Publish as Pub
#global variable
mqtt_data={}


broker = "127.0.0.1" #broker as my local address
topic_name =["topic/rasp4/directions/start", "topic/rasp4/directions/stop"]

log_path=os.system('mkdir -p Log')
rasp_id ="A"
logging.basicConfig(filename= 'Log/rasp'+rasp_id+'.log',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def kill(val, val1):
    print("timer scaduto")
    print("topic/rasp4/directions/stop/" + val)
    Pub.publishing_stop(broker, "topic/rasp4/directions/stop/" + val)
    os.system("mosquitto_pub -h " + broker + " -m "+val1+"  -t " +"topic/rasp4/directions/stop/" + val)

def on_connect(client, obj, flags, rc):
    print("connection result: " + str(rc))




def on_message(client, userdata, msg):


    logging.info("Receiving a msg with payload " + str(msg.payload.decode("utf-8")))
    print("Receiving a msg with payload ", str(msg.payload.decode("utf-8")))
    msg_mqtt_raw = str(msg.payload.decode("utf-8"))
    print(msg.topic)
    print("topic/rasp4/directions/stop/"+str(msg.payload.decode("utf-8"))[0])


    if msg.topic == "topic/rasp4/directions/start":
        logging.info("starting msg is received")

        try:
            if len(msg.payload)>0:
                print("sono dentro il try")
                with open("Thread.txt", "a") as f:
                    f.write(str(msg.payload.decode("utf-8")))
                    f.write("\n")
                    #print("PAYLOAD NON ZERO")
                    logging.info("loading json file "+ str(msg.payload.decode("utf-8")))
                    #print("starting timer")
                    t = threading.Timer(360.0, kill, [str(msg.payload.decode("utf-8"))[0], str(msg.payload.decode("utf-8"))[0]])
                    t.start()
                    t_mqtt = subscribing_thread(topic_name[1]+"/"+str(msg.payload.decode("utf-8"))[0])
                    print(topic_name[1]+"/"+str(msg.payload.decode("utf-8"))[0])
                    t_mqtt.setDaemon(True)
                    t_mqtt.start()

        except ValueError as e:
            logging.error("Malformed json %s. Json: %s", e, msg_mqtt_raw)
            msg_mqtt = msg_mqtt_raw[:-1]
            msg_mqtt = msg_mqtt[1:]

            #print(mqtt_data)
            '''start_msg = StartMsg(id=mqtt_data["id"][0],
                                 mac_address=mqtt_data["mac_address"][0],
                                 place_id=mqtt_data["place_id"][0],
                                 timestamp=mqtt_data["timestamp"][0],
                                 color=mqtt_data["color"][0],
                                 beacon_flag=mqtt_data["beacon_flag"][0])
            print(start_msg)'''

    elif msg.topic == "topic/rasp4/directions/stop/"+str(msg.payload.decode("utf-8"))[0]:
        print("stop message: "+str(msg.payload.decode("utf-8")))
        print("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
        logging.info("Stop tracking")
        os.system("sed -i '/"+msg.topic[-1]+".json/d' ./Thread.txt")
        sys.exit()
        #os.system("pkill -f Main.py")



def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid))
    pass

def on_log(client, obj, level, string):
    print(string)

def print_msg(client, userdata, message):
    print("%s : %s" % (message.topic, message.payload))

class subscribing_thread(threading.Thread):
    def __init__(self, topic_name):
        threading.Thread.__init__(self)
        self.broker="127.0.0.1"
        self.topic_name1=topic_name
        self.client = mqtt.Client()
        #self.topic_name2="topic/rasp4/directions/stop"

    def run(self):

        self.client.on_message=on_message
        print("connecting to broker ", self.broker)
        try:
            print("mi sto connettendo")
            self.client.connect(self.broker)
            print("ce l'ho fatta")
            logging.info("connect to the broker")

        except:
            print("can't connect")
            logging.error("can't connect to broker")
            sys.exit(1)
        print(self.topic_name1)
        #client.loop_start()
        self.client.subscribe(self.topic_name1, qos=1)

        print("Subscribed!\n")
        # client.disconnect()
        #client.loop_stop()
        self.client.loop_forever()







