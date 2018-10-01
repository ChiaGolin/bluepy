#!/usr/bin/python3

import logging
import threading
import json
import queue as Queue
import paho.mqtt.client as mqtt
from collections import namedtuple


def connection_on(client, broker_addr):
    client.connect(broker_addr)

    #subscribing topic
    # 1) StarMsg
    # 2) StopMsg
def subscription(client, topic_name):
    client.subscribe(topic_name, qos=1)
    logging.debug("Subscribing to %s", topic_name)

def publish(client, topic_name, msg):
    client.publish(topic_name, msg)

def connection_off(client):
    client.disconnect()

def on_message(client, msg, topic_name):
    logging.info("Receiving a msg with payload %s", str(msg.payload.decode("utf-8")))
    msg_mqtt_raw = str(msg.payload.decode("utf-8"))
    print("receive a msg in MQTT")

    if msg.topic == topic_name:
        logging.info("starting msg is received")


