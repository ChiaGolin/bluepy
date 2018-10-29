import blescan as ble
from time import strftime, localtime
import json
import Publish as Pub
import random

#broker = "127.0.0.1"
broker = "10.79.1.176"
topic_name ="topic/rasp4/directions/start"
start=input("Do you want to register a new beacon? [y/n]")

if start=="yes":
    MAC_list, BeaconID = ble.Beacon()

    print("1) ANTLAB")
    print("2) ISPG")
    print("3) Room PT2")
    print("4) Bio and Web enginnering LAB")
    print("5) ANTLAB canteen")
    print("6) Alessandro Redond's Office")
    print("7) Matteo Cesana's Office")
    print("8) Antonio Capone's Office")
    print("9) Ilario Filippini's Office")
    print("\n")
    place=input("Which is your final destination?")

    if place=="1":
        placeID="0001"


    if place=="2":
        placeID="0002"


    if place=="3":
        placeID="0003"
        color="pink"

    if place=="4":
        placeID="0004"


    if place=="5":
        placeID="0005"


    if place=="6":
        placeID="3403"


    if place=="7":
        placeID="3695"


    if place=="8":
        placeID="3449"


    if place=="9":
        placeID="3657"


    starting_time = strftime("%H%M%S", localtime())  # hour, minute, second
    starting_day = strftime("%d%m%y", localtime())
    timestamp = starting_time + ' ' + starting_day

    Beacon_flag=1

    color_array=["green", "red", "blue", "yellow", "pink", "brown", "black", "grey"]
    val=random.randint(0, len(color_array)-1)
    print(len(color_array))

    Beacon_dictionary = \
        {
            "id": str(BeaconID[0]),
            "mac": MAC_list,
            "place_id": placeID,
            "timestamp": timestamp,
            "color": color_array[val],
            "beacon_flag": Beacon_flag,

        }

    #json_file=BeaconID[0] + '.json'
    #with open(json_file, 'w') as f:
    #    json_string = json.dump(Beacon_dictionary, f)

    json_file=str(Beacon_dictionary)


    Pub.publishing_start(json_file, broker, topic_name)


'''
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

    with open(BeaconID[0] + '.json', 'w') as f:
        json_string = json.dump(Beacon_dictionary, f)'''
