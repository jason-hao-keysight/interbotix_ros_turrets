##############################################################################################################################
##File:                RPiServoDriver.py                                                                                    ##
##Descripion:          Python Driver for Interbotix wxxms turret connected to Raspberry Pi 4 running Ubuntu 20.04.3 LTS     ##
##Author:              Aaron Wood Keysight Global Solutions Delivery                                                        ##
##Version:             1.0                                                                                                  ##
##Lastest Release:     February 4th, 2021                                                                                   ##
##                                                                                                                          ##
##Unauthorized use, modification, duplication, reverse engineering, any form of redistribution is prohibited                ##
##Please contact Keysight Global Solutions Delivery team for licensing                                                      ##
##############################################################################################################################

import time
import socket
from interbotix_xs_modules.turret import InterbotixTurretXS
import math
import numpy as np
import rospy
import select

scaler = 23860929
degToRad=0.01745329251994329576923690768489
dwell=.5
connection = False
robot = InterbotixTurretXS(
        robot_model="wxxms",
        pan_profile_type="time",
        tilt_profile_type="time")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', 6666))
print ("UDPServer Waiting for client on port 6666")
while connection==False:
    dataFromClient, address = server_socket.recvfrom(1)
    if dataFromClient[0] == 238:
        handshakeReturn = (221).to_bytes(1,byteorder='little')
        print("Connected to client on IP Address ", address)
        server_socket.sendto(handshakeReturn,address)
        connection=True
        inputs = [server_socket]
# Recive data from client and decide which function to call
while not rospy.is_shutdown():
    readable,_,exceptional = select.select(inputs,[],inputs,0.5)
    
    for newData in readable:
        dataFromClient, address = newData.recvfrom(9)
        if ((dataFromClient[0]==204 and connection==True)):
            tiltBytes= dataFromClient[1:5]
            panBytes= dataFromClient[5:9]
            pan = int.from_bytes(panBytes, byteorder='little',signed=True)
            tilt = int.from_bytes(tiltBytes, byteorder='little',signed=True)
            pan/=scaler
            tilt/= scaler
            robot.turret.pan_tilt_move(
                    pan_position=pan*degToRad,
                    tilt_position=tilt*degToRad,
                    pan_profile_velocity=1,
                    pan_profile_acceleration=.1,
                    tilt_profile_velocity=1,
                    tilt_profile_acceleration=.1,
                    blocking=True)
            print(pan)
            print(tilt)
            OPC = (153).to_bytes(1,byteorder='little')
            server_socket.sendto(OPC,address)
        if dataFromClient[0]==187:
            handshakeReturn = (170).to_bytes(1,byteorder='little')
            print("Closed connection on client on IP Address ", address)
            server_socket.sendto(handshakeReturn,address)
            connection=False
        if dataFromClient[0] == 238:
            handshakeReturn = (221).to_bytes(1,byteorder='little')
            print("Connected to client on IP Address ", address)
            server_socket.sendto(handshakeReturn,address)
            connection=True
    for exc in exceptional:
        print("Please Reset Driver")
        sys.exit("Socket Exception")
