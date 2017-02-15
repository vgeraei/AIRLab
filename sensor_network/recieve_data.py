import sys
import sqlite3
from datetime import datetime
from Queue import Queue
from threading import Thread
from collections import deque
import time



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


class XBee():
    RxBuff = bytearray()
    RxMessages = deque()

    def __init__(self, serialport, baudrate=9600):
        self.serial = serial.Serial(port=serialport, baudrate=baudrate)

    def Receive(self):
        """
           Receives data from serial and checks buffer for potential messages.
           Returns the next message in the queue if available.
        """
        remaining = self.serial.inWaiting()
        while remaining:
            chunk = self.serial.read(remaining)
            remaining -= len(chunk)
            self.RxBuff.extend(chunk)

        msgs = self.RxBuff.split(bytes(b'\x7E'))
        for msg in msgs[:-1]:
            self.Validate(msg)

        self.RxBuff = (bytearray() if self.Validate(msgs[-1]) else msgs[-1])

        if self.RxMessages:
            return self.RxMessages.popleft()
        else:
            return None

    def Validate(self, msg):
        """
        Parses a byte or bytearray object to verify the contents are a
          properly formatted XBee message.
        Inputs: An incoming XBee message
        Outputs: True or False, indicating message validity
        """
        # 9 bytes is Minimum length to be a valid Rx frame
        #  LSB, MSB, Type, Source Address(2), RSSI,
        #  Options, 1 byte data, checksum
        if (len(msg) - msg.count(bytes(b'0x7D'))) < 9:
            return False

        # All bytes in message must be unescaped before validating content
        frame = self.Unescape(msg)

        LSB = frame[1]
        # Frame (minus checksum) must contain at least length equal to LSB
        if LSB > (len(frame[2:]) - 1):
            return False

        # Validate checksum
        if (sum(frame[2:3 + LSB]) & 0xFF) != 0xFF:
            return False

        print("Rx: " + self.format(bytearray(b'\x7E') + msg))
        self.RxMessages.append(frame)
        return True

    def SendStr(self, msg, addr=0xFFFF, options=0x01, frameid=0x00):
        """
        Inputs:
          msg: A message, in string format, to be sent
          addr: The 16 bit address of the destination XBee
            (default: 0xFFFF broadcast)
          options: Optional byte to specify transmission options
            (default 0x01: disable acknowledge)
          frameid: Optional frameid, only used if Tx status is desired
        Returns:
          Number of bytes sent
        """
        return self.Send(msg.encode('utf-8'), addr, options, frameid)

    def Send(self, msg, addr=0xFFFF, options=0x01, frameid=0x00):
        """
        Inputs:
          msg: A message, in bytes or bytearray format, to be sent to an XBee
          addr: The 16 bit address of the destination XBee
            (default broadcast)
          options: Optional byte to specify transmission options
            (default 0x01: disable ACK)
          frameod: Optional frameid, only used if transmit status is desired
        Returns:
          Number of bytes sent
        """
        if not msg:
            return 0

        hexs = '7E 00 {:02X} 01 {:02X} {:02X} {:02X} {:02X}'.format(
            len(msg) + 5,  # LSB (length)
            frameid,
            (addr & 0xFF00) >> 8,  # Destination address high byte
            addr & 0xFF,  # Destination address low byte
            options
        )

        frame = bytearray.fromhex(hexs)
        #  Append message content
        frame.extend(msg)

        # Calculate checksum byte
        frame.append(0xFF - (sum(frame[3:]) & 0xFF))

        # Escape any bytes containing reserved characters
        frame = self.Escape(frame)

        print("Tx: " + self.format(frame))
        return self.serial.write(frame)

    def Unescape(self, msg):
        """
        Helper function to unescaped an XBee API message.
        Inputs:
          msg: An byte or bytearray object containing a raw XBee message
               minus the start delimeter
        Outputs:
          XBee message with original characters.
        """
        if msg[-1] == 0x7D:
            # Last byte indicates an escape, can't unescape that
            return None

        out = bytearray()
        skip = False
        for i in range(len(msg)):
            if skip:
                skip = False
                continue

            if msg[i] == 0x7D:
                out.append(msg[i + 1] ^ 0x20)
                skip = True
            else:
                out.append(msg[i])

        return out

    def Escape(self, msg):
        """
        Escapes reserved characters before an XBee message is sent.
        Inputs:
          msg: A bytes or bytearray object containing an original message to
               be sent to an XBee
         Outputs:
           A bytearray object prepared to be sent to an XBee in API mode
         """
        escaped = bytearray()
        reserved = bytearray(b"\x7E\x7D\x11\x13")

        escaped.append(msg[0])
        for m in msg[1:]:
            if m in reserved:
                escaped.append(0x7D)
                escaped.append(m ^ 0x20)
            else:
                escaped.append(m)

        return escaped

    def format(self, msg):
        """
        Formats a byte or bytearray object into a more human readable string
          where each bytes is represented by two ascii characters and a space
        Input:
          msg: A bytes or bytearray object
        Output:
          A string representation
        """
        return " ".join("{:02x}".format(b) for b in msg)

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
            print("Lenght of Q: {0}".format(q.qsize()))
            resp = q.get()
            if q.qsize() > 50:
                with q.mutex:
                    q.queue.clear()
                    print("Queue Cleared!")
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


    # while True:
    #     try:
    #         ser = serial.Serial(PORT + str(usb_counter), BAUD_RATE)
    #         # print("connected")
    #         break
    #     except:
    #         # print(usb_counter)
    #         usb_counter = usb_counter + 1

    while True:
        try:
            xbee = XBee(PORT+ str(usb_counter))
            # print("connected")
            break
        except:
            # print(usb_counter)
            usb_counter = usb_counter + 1


    # Create API object
    # zb = ZigBee(ser, escaped=True)

    # Continuously read and print packets
    light_var = 0
    while True:
        try:
            # print("Before reading")
            # response = zb.wait_read_frame()
            print("Message Sent")
            # q.put(response)
            # print(response)
            if light_var:
                sent = xbee.SendStr("1")
                light_var = 0
                print("sent 1")
            else:
                sent = xbee.SendStr("0")
                light_var = 1
                print("sent 0")

            time.sleep(2)
            # print(response)
            # print("Before Processing")
            # ser.reset_input_buffer()  # Clear the input buffer once we read the data
            # ser.reset_output_buffer()
        except KeyboardInterrupt:
            print("The program has ended by interrupt")
            continue

    # ser.close()

def main_loop():
    print("Receive Data is Running")
    resp_put_thread = Thread(target=resp_put, args=(resp_queue,))
    # resp_put_thread.setDaemon(True)
    resp_put_thread.start()

    # resp_get_thread = Thread(target=resp_get, args=(resp_queue,))
    # resp_get_thread.setDaemon(True)
    # resp_get_thread.start()

    # resp_queue.join()

if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        print >> sys.stderr, '\nExiting by user request.\n'
        sys.exit(0)