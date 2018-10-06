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
#topic_name =["topic/rasp4/directions/start", "topic/rasp4/directions/stop"]

log_path=os.system('mkdir -p Log')
rasp_id ="A"
logging.basicConfig(filename= 'Log/rasp'+rasp_id+'.log',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def on_connect(client, obj, flags, rc):
    print("connection result: " + str(rc))




def on_message(client, userdata, msg):
    global mqtt_data
    mqtt_data={}
    logging.info("Receiving a msg with payload " + str(msg.payload.decode("utf-8")))
    print("Receiving a msg with payload %s", str(msg.payload.decode("utf-8")))
    msg_mqtt_raw = str(msg.payload.decode("utf-8"))
    print(msg.topic)


    if msg.topic == "topic/rasp4/directions/start":
        logging.info("starting msg is received")

        try:
            print("sono dentro il try")
            with open(str(msg.payload.decode("utf-8"))) as f:
                mqtt_data = json.load(f)
                logging.info("loading json file "+ str(msg.payload.decode("utf-8")))

        except ValueError as e:
            logging.error("Malformed json %s. Json: %s", e, msg_mqtt_raw)
            msg_mqtt = msg_mqtt_raw[:-1]
            msg_mqtt = msg_mqtt[1:]

        print(mqtt_data)
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
        os.system("pkill -f Main.py")


#def on_message(client, userdata, message):
 #   time.sleep(1)
  #  print("received message =",str(message.payload.decode("utf-8")))






def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid))
    pass

def on_log(client, obj, level, string):
    print(string)

def print_msg(client, userdata, message):
    print("%s : %s" % (message.topic, message.payload))


def subscription(broker, topic_name):
    if topic_name=="topic/rasp4/directions/start":
        client = mqtt.Client("client-001")
    else:
        client = mqtt.Client("client-002")
    print(mqtt_data)

    client.on_message = on_message
    print("connecting to broker ", broker)
    try:
        print("mi sto connettendo")
        client.connect(broker)
        print("ce l'ho fatta")
        logging.info("connect to the broker")

    except:
        print("can't connect")
        logging.error("can't connect to broker")
        sys.exit(1)

    while len(mqtt_data)<=0:
        client.loop_start()
        print(topic_name)
        client.subscribe(topic_name, qos=1)
       # client.publish(topic_name,'ciaooooooooooooo')
        time.sleep(10)
        #client.disconnect()

        client.loop_stop()
        print("sono qui")
    client.disconnect()
    print("sto per uscire dalla funz sub")
    return mqtt_data

    #client.loop_forever()



#subscription(broker,"topic/rasp4/directions/start")
'''
# create a client
client = mqtt.Client("client-001")
print(topic_name)
logging.info("creation client MQTT")
# callback messages
client.on_subscribe = on_subscribe

client.on_connect = on_connect

print("Connecting to broker " + broker)


# client subscribe both the topic (start and stop)

mqtt_data.clear()

while len(mqtt_data) <= 0:
    client.loop_start()
    client.subscribe(topic_name, qos=1)

    # client.subscribe(topic_name[1], qos=1)
    logging.info("subscribing ... ")
    time.sleep(5)
    print(mqtt_data)
    client.loop_stop()

logging.info("creation of Beacon dictionary: ")
return mqtt_data


 # create client object client1.on_publish = on_publish #assign function to callback client1.connect(broker,port) #establish connection client1.publish("house/bulb1","on")
    ######Bind function to callback
    client.on_message = on_message
    #####
    print("connecting to broker ", broker)
    client.connect(broker)  # connect
    client.loop_start()  # start loop to process received messages
    print("subscribing ")
    client.subscribe(topic_name)  # subscribe
    time.sleep(2)
    print("publishing ")
    client.publish(topic_name, "on")  # publish
    time.sleep(4)
    client.disconnect()  # disconnect
    client.loop_stop()  # stop loop'''