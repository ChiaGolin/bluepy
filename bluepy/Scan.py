#!/usr/bin/env python
from __future__ import print_function
import argparse
import binascii
import os
import sys
from bluepy import btle
import pprint as pp
import blescan2 as ble
import logging
import threading
import queue
from collections import namedtuple
from datetime import datetime
import xml.etree.ElementTree as ET
import xml_parser
import Publish as Pub
from p5 import *
import time
#import prova2
import turtle
#from tkinter import *
if sys.version_info[0] == 2:
    from Tkinter import *
else:
    from tkinter import *
from mttkinter import mtTkinter
import threading





ble_list={}
#MAC=[]
MAcList=[]

#id_place="001"
rasp_id ="A"
logging.basicConfig(filename= 'Log/rasp'+rasp_id+'.log',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

broker = "127.0.0.1" #broker as my local address
broker = "10.79.1.176"
topic_name =["topic/rasp4/directions/start", "topic/rasp4/directions/stop"]
ProjMsg = namedtuple('ProjMsg', ['mac_address', 'direction', 'color', 'status'])

def rssi_info(MAC):
    os.system("l2ping")


def open_map(map_path):
    tree = ET.parse(map_path)
    root = tree.getroot()
    return root

def kill():
    sys.exit()

def kill1(root):
    root.destroy()


def draw_art():


    window = turtle.Screen()
    window.setup(width=1000, height=1000, startx=-0, starty=1000)

    charles = turtle.Turtle()
    charles.shape("arrow")
    charles.color("yellow")
    charles.shapesize(11,6)
    #charles.sety(-400)
    #turtle.goto(10,0)
    charles.speed(1)
    charles.left(90)
    charles.forward(450)

class display(threading.Thread):

    def __init__(self, tk_root, count):
        threading.Thread.__init__(self)
        self.root = tk_root
        self.count=count

    def run(self):

        #time.sleep(self.count)
        self.root.destroy()
        self.root.update()
        sys.exit(1)


class display_thread(threading.Thread):

    def __init__(self, count):
        threading.Thread.__init__(self)
        #self.root = tk_root
        self.count=count


    def run(self):
        root = mtTkinter.Tk()

        canvas = Canvas(root, width=600, height=400)

        canvas.pack()

        points = [250, 110, 480, 200, 280, 280, 250, 110]
        canvas.create_polygon(points, fill="green", outline="green")
        root.mainloop()


'''class draw:
    def __init__(self, direction):
        self.direction=direction

    def setup(self):
        size(640, 360)
        no_stroke()
        no_loop()

    def draw(self):


        background(250)

        if self.direction == "sx":
            background(250)

            fill(204)
            triangle((375, 100), (425, 150), (375, 200))

            fill(204)
            rect((275, 125), 100, 50)

        elif self.direction == "dx":
            background(250)

            fill(204)
            triangle((275, 100), (225, 150), (275, 200))

            fill(204)
            rect((275, 125), 100, 50)

        elif self.direction == "up":
            background(250)

            fill(204)
            triangle((300, 50), (250, 150), (350, 150))

            fill(204)
            rect((275, 150), 50, 100)

        elif self.direction == "back":
            background(250)

            fill(204)
            triangle((250, 225), (300, 275), (350, 225))

            fill(204)
            rect((275, 125), 50, 100)

    def main_draw(self):
        run()'''

def osss(direction):
    os.system("python3 " + direction + ".py")


class read_dictionary:
    def __init__(self, MAcList, id, ble_list, place_id, color,queue, del_queue):
        self.MAcList=MAcList
        self.id=id
        self.ble_list=ble_list
        self.place_id=place_id
        self.color=color
        self.queue=queue
        self.del_queue=del_queue

    def execution(self):
        rssi_list = []
        MAC = []
        return_dict = {}

        first_time=0

        final = None

        root = open_map("map.xml")
        #print(rssi_list)
        #print(self.MAcList)

        for i in range(0, len(self.MAcList)):
            for key, val in self.ble_list.items():
                #print(key)

                if key == self.MAcList[i]:

                    rssi_list.append(val['rssi'])



        rssi = ble.RSSI_ave(rssi_list)
        # rssi = ble.RSSI_max(rssi_list)

        if float(rssi) < (-80.4):
            status = "Really far away"

        if float(rssi) < (-75.5) and float(rssi) >= (-80.4):
            status = "Far away"

        for i in range(0, len(MAcList)):
            for key, val in ble_list.items():
                if key == MAcList[i]:
                    rssi_list.append(val['rssi'])

        # rssi = ble.RSSI_ave(rssi_list)
        # print(rssi)

        if float(rssi) < (-65) and float(rssi) >= (-75.5):
            status = "Is coming"

            direction, final = xml_parser.find_direction(root, self.place_id, rasp_id)

            # turn_on_projector(direction, MAcList, color, proj_queue, status)

            # print(direction)

        if float(rssi) < (-54) and float(rssi) >= (-65):
            status = "Close"

            direction, final = xml_parser.find_direction(root, self.place_id, rasp_id)
            # print(direction)

        if float(rssi) >= (-54):
            status = "Really close"
            direction, final = xml_parser.find_direction(root, self.place_id, rasp_id)

        if final == True:
            Pub.publishing_stop(broker, topic_name[1], id)

        if float(rssi) >= (-72.5):
            print("Beacon " + str(self.id) + "\t" + str(rssi) + "\t" + str(status) + "\t" + str(self.place_id) + "\t" + str(direction))

            return_dict = {"direction": direction,
                           "color": self.color,
                           "id":self.id}

            # pp.pprint(return_dict)


            #print(self.proj_queue.get())
            self.queue.put(return_dict)


        else:
            print("Beacon " + str(self.id) + "\t" + str(rssi) + "\t" + str(status) + "\t" + str(self.place_id))









    count = 1

    '''disp = display_thread(count)
    disp.setDaemon(True)
    disp.start()
    disp.join(1)
'''
    '''root = Tk()

    canvas = Canvas(root, width=600, height=400)

    canvas.pack()

    points = [250, 110, 480, 200, 280, 280, 250, 110]
    canvas.create_polygon(points, fill="green", outline="green")
    # root.destroy()
    # t = threading.Timer(5.0, kill1)
    # t.start()

    # root.after(100, kill1)
    disp = display(root, count)
    disp.setDaemon(True)
    disp.start()
    disp.join(3)
    root.mainloop()'''

    #prova2.draw_art()
    '''draw_val=draw(direction)
    draw_val.setup()
    draw_val.draw()
    draw_val.main_draw()'''


'''  # p=threading.Thread(target=osss, args=(direction,))
#p.start()
#p.join(5)
#time.sleep(5)
#sys.exit()'''
'''  window = turtle.Screen()
window.setup(width=1000, height=1000, startx=-0, starty=1000)
charles = turtle.Turtle()
charles.shape("arrow")
charles.color("yellow")
charles.shapesize(11, 6)
# charles.sety(-400)
# turtle.goto(10,0)
charles.speed(1)
charles.left(90)
charles.forward(450)
#sys.exit()
#turtle.bye()
#turtle.exitonclick()

window.bye()
#turtle.Terminator()
print("nksnksnakds")'''
























