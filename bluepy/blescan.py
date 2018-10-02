#!/usr/bin/env python
import argparse
import binascii
import os
import sys
from bluepy import btle
import pprint as pp
import string
import json
import MAC_Database as MAC
import Publish as pub
from time import strftime, localtime
import logging
from collections import namedtuple

if os.getenv('C', '1') == '0':
    ANSI_RED = ''
    ANSI_GREEN = ''
    ANSI_YELLOW = ''
    ANSI_CYAN = ''
    ANSI_WHITE = ''
    ANSI_OFF = ''
else:
    ANSI_CSI = "\033["
    ANSI_RED = ANSI_CSI + '31m'
    ANSI_GREEN = ANSI_CSI + '32m'
    ANSI_YELLOW = ANSI_CSI + '33m'
    ANSI_CYAN = ANSI_CSI + '36m'
    ANSI_WHITE = ANSI_CSI + '37m'
    ANSI_OFF = ANSI_CSI + '0m'

bluetooth_devices = {}
bd_list = {}
bd_list2 = {}

rasp_id ="A"
logging.basicConfig(filename= 'Log/rasp'+rasp_id+'.log',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


#basic info for MQTT transmition
broker = "127.0.0.1" #broker as my local address
topic_name =["topic/rasp4/directions/start", "topic/rasp4/directions/stop"]
StartMsg = namedtuple('StartMsg', ['mac_address', 'place_id', 'id', 'timestamp', 'color', 'beacon_flag'])
StopMsg = namedtuple('StopMsg', ['mac_address', 'timestamp'])

def dump_services(dev):
    services = sorted(dev.services, key=lambda s: s.hndStart)
    for s in services:
        print("\t%04x: %s" % (s.hndStart, s))
        if s.hndStart == s.hndEnd:
            continue
        chars = s.getCharacteristics()
        for i, c in enumerate(chars):
            props = c.propertiesToString()
            h = c.getHandle()
            if 'READ' in props:
                val = c.read()
                if c.uuid == btle.AssignedNumbers.device_name:
                    string = ANSI_CYAN + '\'' + \
                             val.decode('utf-8') + '\'' + ANSI_OFF
                elif c.uuid == btle.AssignedNumbers.device_information:
                    string = repr(val)
                else:
                    string = '<s' + binascii.b2a_hex(val).decode('utf-8') + '>'
            else:
                string = ''
            print("\t%04x:    %-59s %-12s %s" % (h, c, props, string))

            while True:
                h += 1
                if h > s.hndEnd or (i < len(chars) - 1 and h >= chars[i + 1].getHandle() - 1):
                    break
                try:
                    val = dev.readCharacteristic(h)
                    print("\t%04x:     <%s>" %
                          (h, binascii.b2a_hex(val).decode('utf-8')))
                except btle.BTLEException:
                    break


class ScanPrint(btle.DefaultDelegate):

    def __init__(self, opts):
        btle.DefaultDelegate.__init__(self)
        self.opts = opts

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            status = "new"
        elif isNewData:
            if self.opts.new:
                return
            status = "update"
            return
        else:
            if not self.opts.all:
                return
            status = "old"

        if dev.rssi < self.opts.sensitivity:
            return

        print('    Device (%s): %s (%s), %d dBm %s' %
              (status,
               ANSI_WHITE + dev.addr + ANSI_OFF,
               dev.addrType,
               dev.rssi,
               ('(connectable)' if dev.connectable else '(not connectable)'))
              )
        for (sdid, desc, val) in dev.getScanData():
            if sdid in [8, 9]:
                print('\t' + desc + ': \'' + ANSI_CYAN + val + ANSI_OFF + '\'')
            else:
                print('\t' + desc + ': <' + val + '>')
                manufacturer = (val if 'Manufacturer' in desc else None)

        if not dev.scanData:
            print('\t(no data)')

        bluetooth_devices[dev.addr] = \
            {'rssi': dev.rssi,
             'conn': ('connectable' if dev.connectable else 'not connectable'),
             'add_type': dev.addrType,
             }

        bd_list[dev.addr] = \
            {
                'rssi': dev.rssi
                # 'bd_addr': dev.addr
            }

        bd_list2[dev.addr] = {
            'rssi': dev.rssi
        }
        # minRSSI_bd

        print()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--hci', action='store', type=int, default=0,
                        help='Interface number for scan')
    parser.add_argument('-t', '--timeout', action='store', type=int, default=4,
                        help='Scan delay, 0 for continuous')
    parser.add_argument('-s', '--sensitivity', action='store', type=int, default=-128,
                        help='dBm value for filtering far devices')
    parser.add_argument('-d', '--discover', action='store_true',
                        help='Connect and discover service to scanned devices')
    parser.add_argument('-a', '--all', action='store_true',
                        help='Display duplicate adv responses, by default show new + updated')
    parser.add_argument('-n', '--new', action='store_true',
                        help='Display only new adv responses, by default show new + updated')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Increase output verbosity')
    arg = parser.parse_args(sys.argv[1:])

    btle.Debugging = arg.verbose

    scanner = btle.Scanner(arg.hci).withDelegate(ScanPrint(arg))

    print(ANSI_RED + "Scanning for devices..." + ANSI_OFF)
    devices = scanner.scan(arg.timeout)

    if arg.discover:
        print(ANSI_RED + "Discovering services..." + ANSI_OFF)

        for d in devices:
            if not d.connectable:
                continue

            print("    Connecting to", ANSI_WHITE + d.addr + ANSI_OFF + ":")

            dev = btle.Peripheral(d)
            dump_services(dev)
            dev.disconnect()
            print()


def check(val1, val2, n):
    for i in range(0, n):
        if val2 == val1 + i or val2 == val1 - i or val1 == val2:
            result = 1
            return result
        else:
            result = 0

        return result


def RSSI_ave(list_RSSI):
    average = sum(list_RSSI) / len(list_RSSI)
    return average


if __name__ == "__main__":
    main()

    ble_list=[]
    key_list=[]
    rssi_list=[]
    bd_addr=[]
    mac_list=[]
    BEACON_list=[]

################### create list #################
    for key, val in bd_list.items():
        if key!=None:
            rssi_list.append(int(val['rssi']))
            mac_list.append(str(key))

############# find beacon address (max rssi) ######## if it's the first step

    for key, val in bd_list.items():
        if int(val['rssi'])==max(rssi_list):
            bd_addr.append(key)




############ select from the database all the address associated to the same beacon ############

    print(bd_addr)

    for i in range(0, len(bd_addr)):
        bool_val = 0
        MAC_List=MAC.search_in_DB(bd_addr[i]) #I'll send the list to all the rasberrypi, or just one MAC and I'll find the
        BeaconID = MAC.read_beaconID(MAC_List[0])
        BEACON_list.append(BeaconID)
        RSSI_list=[]

        for i in range(0, len(BEACON_list)):
            # print(BeaconID)
            # print(BEACON_list)
            if BeaconID == BEACON_list[i]:
                bool_val = bool_val + 1

        #print(MAC_List)

        if bool_val<=1:
            if MAC_List != 'not in range':
                print('>>>>>>>> BEACON: '+BeaconID[0])
                for key, val in bd_list.items():
                    if key in MAC_List:
                        if val['rssi'] != None:
                            #print(val['rssi'])
                            RSSI_list.append(int(val['rssi']))

                #print(RSSI_list)
                RSSI_average = RSSI_ave(RSSI_list)
                print(RSSI_average)


                Beacon_flag='1' #######################################------> RENDI A SCELTA
                color='white'####################################---->RENDI A SCELTA
                placeID='3403' #######################################------> RENDI A SCELTA
                starting_time = strftime("%H%M%S", localtime())  # hour, minute, second
                starting_day = strftime("%d%m%y", localtime())
                timestamp=starting_time+' '+starting_day

                #Beacon dictionary
                Beacon_dictionary=\
                {
                    "id":str(BeaconID[0]),
                    "mac":MAC_List,
                    "place_id" :placeID,
                    "timestamp":timestamp,
                    "color":color,
                    "beacon_flag":Beacon_flag,

                }





                with open(BeaconID[0]+'.json', 'w') as f:
                    json_string=json.dump(Beacon_dictionary,f)



                #call the publish, so I can pass the jason file name to the Main
                pub.publishing(BeaconID[0]+'.json', broker, topic_name)


                #print(Beacon_dictionary)


            else:
                print(">>>>> NOT A BEACON")
        else:
            continue




