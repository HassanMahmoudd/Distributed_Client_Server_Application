import sys
import socket
import select
import re
from string import digits
import time

import os

from threading import Thread

import subprocess

from subprocess import Popen, PIPE

import multiprocessing

import paramiko


def start():

    # file = open("system.properties", "r")
    with open('system.properties') as f:
        lines = f.readlines()
        lines = [x.strip() for x in lines]
    #print lines

    server_prop = lines[0].split("=")[1]
    #print server_IP

    server_port = lines[1].split("=")[1]
    #print server_port

    number_of_readers = lines[2].split("=")[1]
    #print number_of_readers

    reader_0_name = lines[3].split("=")[0].split(".")[1]
    #print reader_0_name

    reader_0_prop = lines[3].split("=")[1]
    reader_0_IP = reader_0_prop.split("@")[1]
    reader_0_username = reader_0_prop.split("@")[0]
    #print reader_0_IP

    reader_1_name = lines[4].split("=")[0].split(".")[1]

    reader_1_prop = lines[4].split("=")[1]
    reader_1_IP = reader_1_prop.split("@")[1]
    reader_1_username = reader_1_prop.split("@")[0]


    reader_2_name = lines[5].split("=")[0].split(".")[1]

    reader_2_prop = lines[5].split("=")[1]
    reader_2_IP = reader_2_prop.split("@")[1]
    reader_2_username = reader_2_prop.split("@")[0]


    reader_3_name = lines[6].split("=")[0].split(".")[1]

    reader_3_prop = lines[6].split("=")[1]
    reader_3_IP = reader_3_prop.split("@")[1]
    reader_3_username = reader_3_prop.split("@")[0]

    number_of_writers = lines[7].split("=")[1]
    #print number_of_writers

    writer_0_name = lines[8].split("=")[0].split(".")[1]
    #print writer_0_name
    writer_0_prop = lines[8].split("=")[1]
    writer_0_IP = writer_0_prop.split("@")[1]
    writer_0_username = writer_0_prop.split("@")[0]


    #print writer_0_IP

    writer_1_name = lines[9].split("=")[0].split(".")[1]
    writer_1_prop = lines[9].split("=")[1]
    writer_1_IP = writer_1_prop.split("@")[1]
    writer_1_username = writer_1_prop.split("@")[0]


    writer_2_name = lines[10].split("=")[0].split(".")[1]
    writer_2_prop = lines[10].split("=")[1]
    writer_2_IP = writer_2_prop.split("@")[1]
    writer_2_username = writer_2_prop.split("@")[0]

    writer_3_name = lines[11].split("=")[0].split(".")[1]
    writer_3_prop = lines[11].split("=")[1]
    writer_3_IP = writer_3_prop.split("@")[1]
    writer_3_username = writer_3_prop.split("@")[0]

    number_of_accesses = lines[12].split("=")[1]
    #print number_of_accesses

    server_IP = server_prop.split("@")[1]
    server_username = server_prop.split("@")[0]



    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server_IP, username=server_username, password="123456789")

    print 'running remote command'

    stdin, stdout, stderr = ssh.exec_command("python server.py " + server_IP + " " + server_port + " " + str(60))
    stdin.close()



    print 'connection to %s closed' % "mahmoud"

    # exit()

    thread1 = multiprocessing.Process(target=commands, args=(server_IP, server_port, reader_0_IP, reader_0_name, number_of_accesses, reader_0_username))

    #print "============================================================="

    thread2 = multiprocessing.Process(target=commands, args=(server_IP, server_port, writer_0_IP, writer_0_name, number_of_accesses, writer_0_username))
    #print "============================================================="

    thread3 = multiprocessing.Process(target=commands, args=(server_IP, server_port, reader_1_IP, reader_1_name, number_of_accesses, reader_1_username))
    #print "============================================================="

    thread4 = multiprocessing.Process(target=commands, args=(server_IP, server_port, writer_1_IP, writer_1_name, number_of_accesses, writer_1_username))
    #print "============================================================="

    thread5 = multiprocessing.Process(target=commands,
                                      args=(server_IP, server_port, reader_2_IP, reader_2_name, number_of_accesses, reader_2_username))

    # print "============================================================="

    thread6 = multiprocessing.Process(target=commands,
                                      args=(server_IP, server_port, writer_2_IP, writer_2_name, number_of_accesses, writer_2_username))
    # print "============================================================="

    thread7 = multiprocessing.Process(target=commands,
                                      args=(server_IP, server_port, reader_3_IP, reader_3_name, number_of_accesses, reader_3_username))
    # print "============================================================="

    thread8 = multiprocessing.Process(target=commands,
                                      args=(server_IP, server_port, writer_3_IP, writer_3_name, number_of_accesses, writer_3_username))
    # print "============================================================="

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()
    thread6.start()
    thread7.start()
    thread8.start()


def commands(server_IP, server_port, RW_IP, RW_name, number_of_accesses, RW_username):
    print "============================================================="



    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(RW_IP, username=RW_username, password="123456789")

    print 'running remote command'

    stdin, stdout, stderr = ssh.exec_command("python client.py " + server_IP + " " + server_port + " " + RW_IP + " " + RW_name + " " + number_of_accesses)
    stdin.close()

    print 'connection to %s closed' % "nourhan"

if __name__ == "__main__":
    sys.exit(start())