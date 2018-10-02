import logging
import paho.mqtt.client as mqtt
import sys
import json
import os
from collections import namedtuple
import pprint as pp
import time


#global variable
mqtt_data={}


broker = "127.0.0.1" #broker as my local address
topic_name =["topic/rasp4/directions/start", "topic/rasp4/directions/stop"]

log_path=os.system('mkdir -p Log')
rasp_id ="A"
logging.basicConfig(filename= 'Log/rasp'+rasp_id+'.log',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def on_connect(client, obj, flags, rc):
    print("connection result: " + str(rc))



def on_message(client, userdata, msg):
    global mqtt_data
    logging.info("Receiving a msg with payload " + str(msg.payload.decode("utf-8")))
    print("Receiving a msg with payload %s", str(msg.payload.decode("utf-8")))
    msg_mqtt_raw = str(msg.payload.decode("utf-8"))
    if msg.topic == topic_name[0]:
        logging.info("starting msg is received")

        try:
            with open(str(msg.payload.decode("utf-8"))) as f:
                mqtt_data = json.load(f)
                logging.info("loading json file "+ str(msg.payload.decode("utf-8")))

        except ValueError as e:
            logging.error("Malformed json %s. Json: %s", e, msg_mqtt_raw)
            msg_mqtt = msg_mqtt_raw[:-1]
            msg_mqtt = msg_mqtt[1:]


        '''start_msg = StartMsg(id=mqtt_data["id"][0],
                             mac_address=mqtt_data["mac_address"][0],
                             place_id=mqtt_data["place_id"][0],
                             timestamp=mqtt_data["timestamp"][0],
                             color=mqtt_data["color"][0],
                             beacon_flag=mqtt_data["beacon_flag"][0])
        print(start_msg)'''

    elif msg.topic == topic_name[1]:
        logging.info("Stop tracking")






def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid))


def on_log(client, obj, level, string):
    print(string)

def subscription(broker, topic_name):
    # create a client
    client = mqtt.Client("client-001")
    logging.info("creation client MQTT")
    # callback messages
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    client.on_connect = on_connect

    print("Connecting to broker " + broker)
    try:

        client.connect(broker)
        logging.info("connect to the broker")

    except:
        print("can't connect")
        logging.error("can't connect to broker")
        sys.exit(1)

    # client subscribe both the topic (start and stop)
    print(topic_name[0])
    while len(mqtt_data)<=0:
        client.loop_start()
        client.subscribe(topic_name[0], qos=1)
        client.subscribe(topic_name[1], qos=1)
        logging.info("subscribing ... ")
        time.sleep(10)
        client.loop_stop()

    pp.pprint(mqtt_data["id"][0])
    logging.info("creation of Beacon dictionary: ")
    print("finito, ritorno il dizionario")
    return mqtt_data








