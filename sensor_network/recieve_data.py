import sys
import sqlite3
from datetime import datetime
from Queue import Queue
from threading import Thread



# ####### So we can import models
# import django
# django.setup()
# ####### So we can import models

# from sensor_network.models import *
import json
import serial
import time
from xbee import XBee, ZigBee

realtime_data={'TMP':"23",'LUM':"4.5",'HUM':"3",'NUM':"2",'DST':"0", "PIR":"0"}
temp = 0
light = 0
number = 0
address = 0

sensorNode1_received = 0
sensorNode2_received = 0
sensorNode3_received = 0
sensor_addr1='\x00\x13\xa2\x00\x40\xe9\x99\x36'
sensor_addr2='\x00\x13\xa2\x00\x40\xe9\x97\xc1' #magnet
sensor_addr3='\x00\x13\xa2\x00\x40\xe9\x97\xbe' #number




resp_queue = Queue()
id_counter = 0



def resp_proc(resp):
    print("Reading a response.")
    address = resp['source_addr_long']
    # if (address==temp_sensor_address or address==temp_sensor_address2) :
    # if(True):
    global id_counter
    rf_data = resp['rf_data']
    rf_data = rf_data.replace('\x00', '')
    rf_data = rf_data.strip()
    # name = rf_data[0:3]
    print((rf_data))
    # print(rf_data[4:len(rf_data)])

    wordList = rf_data.split()
    counter = 0
    word = 'ABC'
    value = 0

    for item in wordList:
        if (counter % 2) == 0:
            word = item
        else:
            value = item
            d = datetime.now()
            try:
                c.execute('INSERT INTO sensor_network_sensor VALUES (?,?,?,?)', [id_counter, value, word, d])
            except:
                print("Database error")
            # print(id_counter)
            id_counter = id_counter + 1
            conn.commit()
            realtime_data[word] = value
            realtime_json = json.dumps(realtime_data)

            try:
                with open('realtime_data.json', 'w') as outfile:
                    json.dump(realtime_json, outfile)
            except:
                print("Opening JSON error")
            # print(realtime_data)

        counter = counter + 1

def resp_get(q):
    print("Response getter thread is running.")
    print(type(q.qsize()))
    global id_counter
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    try:
        cursor = c.execute('SELECT max(id) FROM sensor_network_sensor')
        max_id = cursor.fetchone()[0]
        id_counter = max_id + 1
    except:
        id_counter = 1
    while True:
        if not q.empty():
            print("Lenght of Q: ", q.qsize())
            if q.qsize() > 50:
                with q.mutex:
                    q.queue.clear()
                    print("Queue Cleared!")
            resp = q.get()
            q.task_done()
            # print("Reading a response.")
            address = resp['source_addr_long']
            # if (address==temp_sensor_address or address==temp_sensor_address2) :
            # if(True):
            global id_counter
            rf_data = resp['rf_data']
            rf_data = rf_data.replace('\x00', '')
            rf_data = rf_data.strip()
            # name = rf_data[0:3]
            print((rf_data))
            # print(rf_data[4:len(rf_data)])

            wordList = rf_data.split()
            counter = 0
            word = 'ABC'
            value = 0

            for item in wordList:
                if (counter % 2) == 0:
                    word = item
                else:
                    value = item
                    d = datetime.now()
                    try:
                        c.execute('INSERT INTO sensor_network_sensor VALUES (?,?,?,?)', [id_counter, value, word, d])
                    except:
                        print("Database error")
                    # print(id_counter)
                    id_counter = id_counter + 1
                    conn.commit()
                    realtime_data[word] = value
                    realtime_json = json.dumps(realtime_data)

                    try:
                        with open('realtime_data.json', 'w') as outfile:
                            json.dump(realtime_json, outfile)
                    except:
                        print("Opening JSON error")
                        # print(realtime_data)

                counter = counter + 1

def resp_put(q):
    print("Response putter thread is running.")
    PORT = '/dev/ttyUSB'
    BAUD_RATE = 9600
    data_dict = {'TMP': 0, 'LIG': 0, 'HUM': 0, 'NUM': 0, 'MAG': 0}
    # Open serial port
    usb_counter = 0
    while True:
        try:
            ser = serial.Serial(PORT + str(usb_counter), BAUD_RATE)
            # print("connected")
            break
        except:
            # print(usb_counter)
            usb_counter = usb_counter + 1

    # Create API object
    zb = ZigBee(ser, escaped=True)

    # Continuously read and print packets
    while True:
        try:
            # print("Before reading")
            response = zb.wait_read_frame()
            print("Message Received")
            q.put(response)
            # print(response)
            # print("Before Processing")
            # ser.reset_input_buffer()  # Clear the input buffer once we read the data
            # ser.reset_output_buffer()
        except KeyboardInterrupt:
            print("The program has ended by interrupt")
            continue

    ser.close()

def main_loop():
    print("Receive Data is Running")
    resp_put_thread = Thread(target=resp_put, args=(resp_queue,))
    # resp_put_thread.setDaemon(True)
    resp_put_thread.start()

    resp_get_thread = Thread(target=resp_get, args=(resp_queue,))
    # resp_get_thread.setDaemon(True)
    resp_get_thread.start()

    resp_queue.join()

if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        print >> sys.stderr, '\nExiting by user request.\n'
        sys.exit(0)