# chat_server.py

import sys
import socket
import select
from threading import Thread
import threading
import time
from RWlockR import ReadWriteLock
import random
import keyboard
import multiprocessing


server_log_path = "statistics/server_log"
documents_path = "documents/"

RECV_BUFFER = 4096

request_sequence = 1
service_sequence = 1

# SOCKET_LIST = []
HOST = ''
PORT = 9009

THREAD_LIST = []

readers_data = []
writers_data = []

number_of_readers_in_document = {}

# readers_data = [[1,2,3,4,11],[5,6,7,8,11]]
# writers_data = [[1,2,3,9],[4,5,6,9]]

rwlock = ReadWriteLock()
request_sequence_mutex = threading.Lock()
service_sequence_mutex = threading.Lock()
number_of_readers_in_document_mutex  = threading.Lock()


def print_actions():
    global readers_data
    global writers_data

    readers_data = sorted(readers_data, key=lambda x: x[0])
    writers_data = sorted(writers_data, key=lambda x: x[0])

    log = ""
    log += "Readers:\n\n"
    log += ('{0:4s} {1:4s} {2:4s} {3:4s} {4:4s}\n'.format("sSeq", "oID", "oVal", "rID", "rNum"))

    for row in readers_data:
        log += ('{0:^4d} {1:^4s} {2:^4s} {3:^4s} {4:^4s}\n'.format(row[0], row[1],
                                                                   row[2], row[3], row[4]))

    log += "\nWriters:\n\n"
    log += ('{0:4s} {1:4s} {2:4s} {3:4s}\n'.format("sSeq", "oID", "oVal", "wID"))

    for row in writers_data:
        log += ('{0:^4d} {1:^4s} {2:^4s} {3:^4s}\n'.format(row[0], row[1], row[2], row[3]))

    print
    print
    print "######################################################"
    print log
    print "######################################################"
    print
    print
    f = open(server_log_path, "w+")
    f.write(log)
    f.close()

# readers_data = [[1,2,3,4,11],[0,6,7,8,11]]
# writers_data = [[1,2,3,9],[4,5,6,9]]
# print_actions()
# exit()

def serve(request, socket):
    print request
    global readers_data
    global writers_data
    global request_sequence
    global service_sequence
    global rwlock
    global request_sequence_mutex
    global service_sequence_mutex
    global number_of_readers_in_document


    request_parameters = request.split(",")

    if (request_parameters[0] == "r" and len(request_parameters) == 3):
        request_type, machine_id, document_id = request_parameters

    elif (request_parameters[0] == "w" and len(request_parameters) == 4):
        request_type, machine_id, document_id, new_content = request_parameters

    else:
        print "Wrong Request Format"
        return

    path = documents_path + document_id + ".txt"

    request_sequence_mutex.acquire()

    request_id = request_sequence
    request_sequence += 1  # mutex

    request_sequence_mutex.release()



    if(request_parameters[0] == "r"):

        ##mutex
        number_of_readers_in_document_mutex.acquire()

        if number_of_readers_in_document.has_key(document_id):
            number_of_readers_in_document[document_id] += 1
        else:
            number_of_readers_in_document[document_id] = 1

        number_of_readers_in_document_mutex.release()

        # mutex
        timeout_flag = rwlock.acquire_read()

        if not timeout_flag:

            f = open(path, 'r+')
            content = f.read()
            time.sleep(random.randint(0,10000)/1000)
            f.close()
            rwlock.release_read()

            service_sequence_mutex.acquire()

            service_id = service_sequence
            service_sequence += 1  # mutex

            service_sequence_mutex.release()

            packet_msg = str(request_id) + "," + str(service_id) + "," + str(content)
            try:
                socket.send(packet_msg)
            except:
                # broken socket connection
                socket.close()
                # broken socket, remove it
                print "Broken Socket Exception"
                return
            readers_data.append([(service_id), str(document_id), str(content), str(machine_id),
                                str(number_of_readers_in_document[document_id])])

            # mutex
            number_of_readers_in_document_mutex.acquire()

            number_of_readers_in_document[document_id] -= 1

            number_of_readers_in_document_mutex.release()

    else:

        # mutex
        timeout_flag = rwlock.acquire_write()

        if not timeout_flag:


            f = open(path, 'w+')
            f.write(new_content)
            time.sleep(random.randint(0,10000)/1000)
            f.close()
            rwlock.release_write()


            service_sequence_mutex.acquire()

            service_id = service_sequence
            service_sequence += 1  # mutex

            service_sequence_mutex.release()

            packet_msg = str(request_id) + "," + str(service_id)

            try:
                socket.send(packet_msg)
            except:
                # broken socket connection
                socket.close()
                # broken socket, remove it
                print "Broken Socket Exception"
                return

            writers_data.append([(service_id), str(document_id), str(new_content), str(machine_id)])

    if timeout_flag:
        try:
            socket.send("No")
        except:
            # broken socket connection
            socket.close()
            # broken socket, remove it
            print "Broken Socket Exception"
            return
    socket.close




def chat_server():
    if (len(sys.argv) < 4):
        print 'Usage : python server.py hostname port time'
        sys.exit()

    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    server_time_up = int(sys.argv[3])

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)

    print "Server Started On port " + str(PORT) + " On " + time.ctime()

    start_time = time.time()

    while 1:

        # get the list sockets which are ready to be read through select
        # 4th arg, time_out  = 0 : poll and never block
        # if keyboard.is_pressed('a'):
        #     break
        if (time.time() - start_time > server_time_up):
            break
        ready_to_read, ready_to_write, in_error = select.select([server_socket], [], [], 0)

        for sock in ready_to_read:
            # a new connection request recieved
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                print "Client (%s, %s) connected" % addr

                try:
                    request = (sockfd.recv(RECV_BUFFER)).decode("utf-8")
                    # print request
                except:
                    print "Timeout For Client (%s, %s)" % addr
                    continue


                thread = Thread(target=serve, args=(request, sockfd))
                THREAD_LIST.append(thread)
                thread.start()


    print "Server Stoped On Port " + str(PORT) + " On " + time.ctime()
    print "Creating Server Logs"
    print_actions()
    server_socket.close()


if __name__ == "__main__":
    sys.exit(chat_server())
