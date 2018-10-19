import logging
import paho.mqtt.client as mqtt
import sys
import json
import os
import ast
from collections import namedtuple
import pprint as pp
import time
from threading import *

import threading
import Publish as Pub
#global variable
mqtt_data={}


broker = "127.0.0.1" #broker as my local address
broker = "10.79.1.176"
topic_name =["topic/rasp4/directions/start", "topic/rasp4/directions/stop"]

log_path=os.system('mkdir -p Log')
rasp_id ="A"
logging.basicConfig(filename= 'Log/rasp'+rasp_id+'.log',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def kill(val, val1):
    print("timer scaduto")
    print("topic/rasp4/directions/stop/" + val)
    Pub.publishing_stop(broker, "topic/rasp4/directions/stop/" + val)
    os.system("mosquitto_pub -h " + broker + " -m "+val1+"  -t " +"topic/rasp4/directions/stop/" + val)



def on_connect(self, client, obj, flags, rc):
    print("connection result: " + str(rc))

def json_file(dict):

    json_file=dict["id"] + '.json'
    with open(json_file, 'w') as f:
        json.dump(dict, f)

    return json_file

class Receive_on_message:

    def __init__(self, queue_sub, del_queue):
        self.queue_sub = queue_sub
        self.del_queue=del_queue




    def on_message(self, client,userdata, msg):



        logging.info("Receiving a msg " )
        print("Receiving a msg with payload ")
        #str(msg.payload.decode("utf-8")
        Msg = str(msg.payload.decode("utf-8"))




        if msg.topic == "topic/rasp4/directions/start":
            logging.info("starting msg is received")

            json_name=json_file(ast.literal_eval(Msg))



            if len(msg.payload)>0:
                self.queue_sub.put(json_name) #scrive il nome del json file
                logging.info("loading json file "+ str(msg.payload.decode("utf-8")))
                t = threading.Timer(360.0, kill, [str(msg.payload.decode("utf-8"))[0], str(msg.payload.decode("utf-8"))[0]])
                t.start()
                '''start_msg = StartMsg(id=mqtt_data["id"][0],
                                     mac_address=mqtt_data["mac_address"][0],
                                     place_id=mqtt_data["place_id"][0],
                                     timestamp=mqtt_data["timestamp"][0],
                                     color=mqtt_data["color"][0],
                                     beacon_flag=mqtt_data["beacon_flag"][0])
                print(start_msg)'''

        elif msg.topic == "topic/rasp4/directions/stop":

            print("stop message: "+str(msg.payload.decode("utf-8")))
            logging.info("Stop tracking")
            self.del_queue.put(Msg) # scrive il nome del json file






def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid))
    pass

def on_log(client, obj, level, string):
    print(string)

def print_msg(client, userdata, message):
    print("%s : %s" % (message.topic, message.payload))

class subscribing_thread(threading.Thread):
    def __init__(self, topic_name, queue, del_queue):
        threading.Thread.__init__(self)
        self.broker="10.79.1.176"
        self.topic_name1=topic_name
        self.client = mqtt.Client()
        self.queue = queue
        self.del_queue = del_queue
        #self.topic_name2="topic/rasp4/directions/stop"

    def run(self):
        receiver =  Receive_on_message(self.queue, self.del_queue)

        #self.client.on_message=Receive_on_message.on_message
        self.client.on_message= receiver.on_message
        print("connecting to broker ", self.broker)
        try:
            self.client.connect(self.broker)
            logging.info("connect to the broker")

        except:
            print("can't connect")
            logging.error("can't connect to broker")
            sys.exit(1)

        #client.loop_start()


        self.client.subscribe(self.topic_name1[0], qos=1)
        self.client.subscribe(self.topic_name1[1], qos=1)

        print("Subscribed!\n")
        self.client.loop_forever()







