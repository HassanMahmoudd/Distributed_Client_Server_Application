# chat_client.py

import sys
import socket
import select
import re
from string import digits
import time


def chat_client():
    if (len(sys.argv) < 3):
        print 'Usage : python chat_client.py hostname port'
        sys.exit()

    server_IP = sys.argv[1]
    server_port = int(sys.argv[2])
    client_IP = sys.argv[3]
    client_name = sys.argv[4]
    number_of_access = int(sys.argv[5])

    client_ID = map(int, re.findall('\d+', client_name))
    client_ID = client_ID[0]
    client_type = client_name.translate(None, digits)

    print server_IP
    print server_port
    print client_name
    print number_of_access
    print client_ID
    print client_type

    # client_ID = 0
    # client_type = "writer"
    # number_of_access = 3

    rSeq = 0
    sSeq = 0
    oVal = 0

    file = open("log" + str(client_ID), "w")
    if (client_type == "reader"):
        file.write("Client type: " + client_type + "\n")
        file.write("Client name: " + str(client_ID) + "\n")
        #file.write("rSeq    sSeq    oVal\n")
        file.write('{0:7s} {1:7s} {2:7s}\n'.format("rSeq", "sSeq", "oVal"))

    else:
        file.write("Client type: " + client_type + "\n")
        file.write("Client name: " + str(client_ID) + "\n")
        #file.write("rSeq    sSeq\n")
        file.write('{0:7s} {1:7s}\n'.format("rSeq", "sSeq"))

    while 1:


        if(client_type == "reader"):

            if number_of_access == 0:
                break

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)

            # connect to remote host
            while 1:
                try:
                    s.connect((server_IP, server_port))
                    break
                except:
                    print 'Unable to connect'


            print 'Connected to remote host. You can start sending messages'

            socket_list = [s]


            s.send("r" + "," + str(client_ID) + ",1")
            print "\nData sent"
            number_of_access = number_of_access - 1
            print  number_of_access

            # Get the list sockets which are readable
            ready_to_read, ready_to_write, in_error = select.select(socket_list, [], [])

            for sock in ready_to_read:
                if sock == s:
                    # incoming message from remote server, s
                    data_bytes = sock.recv(4096)
                    data = data_bytes.decode("utf-8")

                    print data
                    time.sleep(1)
                    if (data == "No"):
                        #rSeq = rSeq + 1
                        number_of_access = number_of_access + 1
                        continue


                    data = data.split(",")
                    rSeq = data[0]
                    sSeq = data[1]
                    oVal = data[2]


                    if not data:
                        print '\nData is corrupted'
                        sys.exit()

                    else:

                        #file.write(str(rSeq) + "       " + str(sSeq) + "       " + str(oVal) + "\n")
                        file.write('{0:^7s} {1:^7s} {2:^7s}\n'.format(str(rSeq), str(sSeq), str(oVal)))

        else:

            if number_of_access == 0:
                break

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)

            # connect to remote host
            while 1:
                try:
                    s.connect((server_IP, server_port))
                    break
                except:
                    print 'Unable to connect'

            print 'Connected to remote host. You can start sending messages'

            socket_list = [s]

            s.send("w" + "," + str(client_ID) + ",1," + str(client_ID))
            print "\nData sent"
            number_of_access = number_of_access - 1
            print  number_of_access

            # Get the list sockets which are readable
            ready_to_read, ready_to_write, in_error = select.select(socket_list, [], [])

            for sock in ready_to_read:
                if sock == s:
                    # incoming message from remote server, s
                    data_bytes = sock.recv(4096)
                    data = data_bytes.decode("utf-8")
                    print data


                    if(data == "No"):
                        #rSeq = rSeq + 1
                        number_of_access = number_of_access + 1
                        continue
                    data = data.split(",")
                    rSeq = data[0]
                    sSeq = data[1]


                    if not data:
                        print '\nData is corrupted'
                        sys.exit()
                    else:
                        #file.write(str(rSeq) + "       " + str(sSeq) + "\n")
                        file.write('{0:^7s} {1:^7s}\n'.format(str(rSeq), str(sSeq)))

        import random
        time.sleep(random.randint(0, 5))

    # s.close()
    file.close()

if __name__ == "__main__":
    sys.exit(chat_client())