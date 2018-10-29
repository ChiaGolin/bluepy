import threading
import time
import json
import logging
import os
from collections import namedtuple
from tkinter import *
from mttkinter import mtTkinter
import queue
from p5 import *

#my imports

import Subscribe as Sub
import Scan
import blescan2 as ble
import Arrow


log_path=os.system('mkdir -p Log')
rasp_id ="A"
#place_id="0001"

logging.basicConfig(filename= 'Log/rasp'+rasp_id+'.log',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


logging.debug("Start smart directions on rasp "+rasp_id)

#basic info for MQTT transmition
broker = "127.0.0.1" #broker as my local address
#broker = "10.79.1.176"
topic_name =["topic/rasp4/directions/start", "topic/rasp4/directions/stop"]
StartMsg = namedtuple('StartMsg', ['mac_address', 'place_id', 'id', 'timestamp', 'color', 'beacon_flag'])
StopMsg = namedtuple('StopMsg', ['mac_address', 'timestamp'])

BUF_SIZE = 10

global root


def move_b():
    canvas.move(b, 1, 0)
    # move again after 25ms (0.025s)
    root.after(25, move_b)

class display(threading.Thread):
    def __init__(self, queue, direction, color):
        threading.Thread.__init__(self)
        self.queue=queue
        self.direction=direction
        self.color=color

    def run(self):
        print("sono dentro il display thread")

        root = mtTkinter.Tk()
        canvas = Canvas(root, width=600, height=400)

        canvas.pack()

        points = Arrow.arrow(self.direction)
        canvas.create_polygon(points, fill=self.color, outline=self.color)

        root.after(7000, root.destroy)

        root.mainloop()
        self.queue.put("Print again")






class user(threading.Thread):
    def __init__(self, data):
        threading.Thread.__init__(self)
        self.data = data


    def run(self):

        image=0

        direction_queue=queue.Queue() #queue to receive direction and coloro for arrow
        del_direction_queue=queue.Queue()
        root_queue=queue.Queue()
        MAcList = []
        for i in range(0, len(self.data["mac"])):
            MAcList.append(self.data["mac"][i])  # list of MAC of i-th beacon

        global bl_list
        while True:
            print(self.data["color"])
            SCAN = Scan.read_dictionary(MAcList, self.data["id"], ble_list, self.data["place_id"], self.data["color"],direction_queue, del_direction_queue)
            SCAN.execution()
            time.sleep(1)

            if not direction_queue.empty():
                arrow = direction_queue.get()
                direction=arrow["direction"]
                color=arrow["color"]
                if image==0:


                    DISPLAY=display(root_queue, direction, color)
                    DISPLAY.setDaemon(True)
                    DISPLAY.start()
                    image=1

                if not root_queue.empty():
                    print(root_queue.get())
                    image=0










if __name__ == "__main__":


    threads="None"
    THREADS=[]
    array_dict=[]
    size=0
    bl_list={}
    arrow={}
    id_list=[]
    prov={}
    current_users=[]
    root_list=[]
    root=None
    new_user=0
    number_of_user=0

    open("Thread.txt", 'w').close()


  #  mqtt_Data = {}
#
    logging.info("*******************************************")
    logging.info("STARTING MAIN")
    logging.info("*******************************************")


    logging.info("*******************************************")
    logging.info("MQTT SUBSCRIPTION")
    logging.info("*******************************************")


    # do some other stuff in the main process
    sub_q=queue.Queue(BUF_SIZE)
    del_q = queue.Queue(BUF_SIZE)
    data_queue = queue.Queue(BUF_SIZE)
    #proj_queue=queue.Queue(BUF_SIZE)




    t_mqtt = Sub.subscribing_thread(topic_name, sub_q, del_q)
    t_mqtt.setDaemon(True)
    t_mqtt.start()


    while True:
        #canc=0


        #pp.pprint(ble_list)



        if not sub_q.empty():

            threads=sub_q.get()
            #print("thread: "+threads)

            with open(threads) as f:
                try:
                    json_file=json.load(f)
                    #print(json_file)
                    new_user=1
                    number_of_user=number_of_user+1




                except:
                    print("Malformed json")

        if number_of_user>0:
            #print("number of user: " + str(number_of_user))

            ble_list = ble.ScanScan()
            #global ble_list
            #print("new user flag: "+ str(new_user))
            if new_user==1:
                #crea nuovo user thread
                NEW_USER=user(json_file)
                NEW_USER.setDaemon(True)
                NEW_USER.start()

                new_user=0











