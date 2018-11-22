import threading
import time
import json
import logging
import os
from collections import namedtuple
from tkinter import *
from mttkinter import mtTkinter
import queue
import datetime

#my imports

import Subscribe as Sub
import SCAN
import blescan2 as ble
import Arrow
import ppp3
import pprint as pp
import DISPLAY


log_path=os.system('mkdir -p Log')
rasp_id ="b"
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


class user(threading.Thread):
    def __init__(self, data,ble_list_send, delate_user, direction_q, del_direction_q):
        threading.Thread.__init__(self)
        self.data = data #dizionario relativo ai mac
        self.ble_list_send=ble_list_send
        self.delate_user=delate_user
        self.direction_q=direction_q
        self.del_direction_q=del_direction_q


    def run(self):

        # QUEUE
        exit = queue.Queue(1)  # coda sulla quale viene inviato un pacchetto nel momento che o l'id è arrivato


        # VARIABLE
        new = 1
        EXIT = 0
        EXIT_STATUS=None

        #ARRAY
        MAcList = []  # lista dei mac che dovrò controllare

        for i in range(0, len(self.data["mac"])):
            MAcList.append(self.data["mac"][i])  # list of MAC of i-th beacon

        #global ble_list
        print(("per il beacon "+self.data["id"])+ " la lista dei MAC è "+ str(MAcList))
        while EXIT == 0:
            ble_list=self.ble_list_send.get()
            # faccio partire lo scan infinito solo una volta
            if new == 1:
                SCANs=SCAN.Scan_list(MAcList, ble_list, self.data["place_id"], self.data["id"], self.data["color"], exit, self.direction_q, self.del_direction_q)
                SCANs.setDaemon(True)
                SCANs.start()
                new=0

            if not exit.empty():
                EXIT_STATUS=exit.get()

                if EXIT_STATUS=="stop":
                    print("timer_expired")
                else:
                    print(self.data['id']+" is arrived ")

                EXIT=1

        sys.exit()



class Thread_Thread(threading.Thread):
    def __init__(self,arrow_display, wait):
        threading.Thread.__init__(self)
        self.arrow_display=arrow_display
        self.wait=wait

    def run(self):
        DISP = DISPLAY.DisplayArrow(self.arrow_display, self.wait)
        DISP.Go()  # si blocca dentro



class arrow_Thread(threading.Thread):
    def __init__(self, change_add, change_del, kill_direction):
        threading.Thread.__init__(self)
        self.change_add=change_add
        self.change_del=change_del
        self.kill_direction=kill_direction



    def run(self):
        list_arrow=[] #lista degli arrow id

        arrow_display=queue.Queue(1)
        wait=queue.Queue(1)
        i_kill=""




        THREAD_THREAD = Thread_Thread(arrow_display, wait)
        THREAD_THREAD.setDaemon(True)
        THREAD_THREAD.start()


        while True:



            if not self.change_add.empty():
                print("entrato in change add")
                prov_add=self.change_add.get()
                list_arrow.append(prov_add)
                print(list_arrow)

            if not self.change_del.empty():
                print("entrato in change del")
                prov_del=self.change_del.get()
                for i in range(0, len(list_arrow)):
                    if list_arrow[i]["id"]==prov_del["id"]:
                        idx=i
                        break

                del list_arrow[idx]



            if len(list_arrow)>0:

                print(str(list_arrow))

                for i in range(0, len(list_arrow)):
                    print("sono nel for1")
                    print("----------------------------------"+list_arrow[i]["direction"])
                    print("sono nel for2")
                    arrow_display.put(list_arrow[i])
                    print("sono nel for3")

                    wait.get()

                    print("sono nel for1 post wait")

            if not self.kill_direction.empty():
                ID=self.kill_direction.get()
                for i in range(0, len(list_arrow)):
                    if list_arrow[i]["id"]==ID:
                        i_kill=i
                if i_kill!=None:
                    del list_arrow[i_kill]
                    i_kill=None










if __name__ == "__main__":

    #QUEU
    sub_q=queue.Queue(BUF_SIZE) #coda che riceve la subscript
    del_q=queue.Queue(BUF_SIZE) #coda su cui invio la publish stop
    ble_list_send=queue.Queue(BUF_SIZE) #coda che aggiorna sulla scan la lista dei MAC
    delate_user=queue.Queue(BUF_SIZE) #coda sulla quale scrivo chi devo cancellare
    direction_q=queue.Queue(BUF_SIZE)#coda che connette main e scan per aggiunta freccia
    del_direction_q=queue.Queue(BUF_SIZE)#coda che connette main e scan per rimozione freccia
    change_add=queue.Queue(BUF_SIZE) #coda che mi indica che ho un cambiamento e devo aggiungere una freccia
    change_del=queue.Queue(BUF_SIZE) #coda che mi indica che ho un cambiamento e devo eliminare una freccia
    kill_direction=queue.Queue(BUF_SIZE) #coda che serve per togliere definitivamente un user che è arrivato


    #ARRAY
    id_list=[] #list of id in the system



    #VARIABLE
    number_of_user=0
    new_user=0











    t_mqtt = Sub.subscribing_thread(topic_name, sub_q, del_q)
    t_mqtt.setDaemon(True)
    t_mqtt.start()

    ARROW = arrow_Thread(change_add, change_del, kill_direction)
    ARROW.setDaemon(True)
    ARROW.start()

    while True:


        if not sub_q.empty():
            threads = sub_q.get()
            print(str(datetime.datetime.now()) + " sub_q.get " + str(threads))
            print("SUBSCRIBE->MAIN5")

            with open(threads) as f:
                try:
                    json_file = json.load(f)

                    if json_file["id"] not in id_list:
                        id_list.append(json_file["id"])
                        new_user = 1 #It means that the json_file belongs to anew user

                        number_of_user = number_of_user + 1 #increase the number of the users in the system


                except:
                    print("Malformed json")


        if number_of_user>0:

            ble_list = ble.ScanScan()
            #ble_list_send.put(ble_list)


            if new_user==1:

                print("NEW USER")

                NEW_USER=user(json_file, ble_list_send,delate_user, direction_q, del_direction_q)
                NEW_USER.setDaemon(True)
                NEW_USER.start()


                new_user=0

            for i in range(0, len(id_list)):
                ble_list_send.put(ble_list)
                print("INVIATOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")


        if not direction_q.empty():
            print("--------------------------------------------DIRECTION Q")
            dir_prov=direction_q.get()
            change_add.put(dir_prov)

        if not del_direction_q.empty():
            print("DEL DIRECTION Q")

            dir_prov = del_direction_q.get()
            change_del.put(dir_prov)

        if not del_q.empty():
            print("SUBSCRIBING STOP ARRIVED")
            number_of_user=number_of_user-1
            id=del_q.get()

            for i in range(0, len(id_list)):
                if id_list==id:
                    idx=i

            del id_list[idx] #non c'è pericolo che non esista perchè nell'id list c'è tutta la lista dei beacon che sono nel sistema
            kill_direction.put(id)







