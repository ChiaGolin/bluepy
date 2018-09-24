import sqlite3
import time


conn=sqlite3.connect('MAC_database.db')
c=conn.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS Beacon( beacon text, MAC text)')


def data_entry():
    c.execute("INSERT INTO Beacon VALUES('A', 'e1:ab:9e:42:aa:0a')")
    conn.commit()
    c.close()
    conn.close()

def dynamic_data_entry(beacon, MAC):
    c.execute("INSERT INTO Beacon (beacon, MAC) VALUES (?,?)",
              (beacon, MAC))
    conn.commit()


def read_beaconID(val):
    c.execute('SELECT beacon FROM Beacon WHERE beacon IS NOT NULL AND MAC=(?)', [val])


    #print(c.fetchall())
    BeaconID=[]

    for row in c.fetchall():

       BeaconID.append(str(row[0][0]))
       #print('>>>>>>>>>>>BEACON: '+row[0][0])


    return BeaconID


def read_MAClist(BeaconID):

    list=[]

    c.execute('SELECT MAC FROM Beacon WHERE MAC IS NOT NULL AND beacon=(?)', (BeaconID,))


    for row in c.fetchall():

        list.append(row[0])
      #  print(list)

   # print(list)

    return list




def create_db():

    create_table()
    ans=input("Do you need to insert a new line: [y/n]")
    while ans=='y':
        beacon=input("Insert Beacon: ")
        MAC=input("insert MAC: ")
        dynamic_data_entry(beacon, MAC)
        time.sleep(1)
        ans = input("Do you need to insert a new line: [y/n]")


def search_in_DB(MAC):
    conn = sqlite3.connect('MAC_database.db')
    c = conn.cursor()
    MAC_List=[]
    BeaconID=read_beaconID(MAC)


    if len(BeaconID)>0:
        #print(BeaconID[0][0])
        MAclist=read_MAClist(BeaconID[0][0])

        for i in range(0, len(MAclist)):
            MAC_List.append(MAclist[i])

        #print(MAC_List[0])
        c.close()
        conn.close()
        return MAC_List
    else:
        return "not in range"


