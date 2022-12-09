"""
This is the picking cubes on table 1
and places them on the home area at table 1
"""
import urx
from threading import Thread
from Gripper import *
import urllib.request
import sys
import time
picObjectFhinis = False

# set robot ip address
# this is the left robot
r1 = "10.1.1.6"
# this is the right robot
r2 = "10.1.1.5"

# connects to robot
rob = urx.Robot(r1, use_rt=True, urFirm=5.1)
rob2 = urx.Robot(r2, use_rt=True, urFirm=5.1)
# robot velocity and acceleration
v = 0.8
a = 0.5
#stop_threads = False
#robot_moving = True
#robot2_moving = True
#start_time = time.time()
# variables
# these x and y values are the distance from the robot base to the middle of the camera
x = float(25 / 1000)
y = float(-385 / 1000)
lasty = y
lastx = x
objectLocated = 0
objectCount = 0
table2PositionCount = 0
x2 = 0
y2 = 0
x2i = 0
y2i = 0


# positions x, y, z, rx, ry, rz
clearCamera = 0.25, -0.22, 0.20, 0, 3.14, 0
# placeObject = 0.3, -0.25, 0.15, 0, 3.14, 0
placeObject = 0.3, -0.25, 0.03, 0, 3.14, 0  # coordinate to please the block carefully table 1
placeConveyorA = 0.2, 0.3, 0.0013, 2.24, 2.2, 0
overpickPlaceConveyorA = 0.2, 0.3, 0.1, 2.24, 2.2, 0
pickConveyorA = 0, 0.3, 0.15, 0, 3.14, 0
pickVia = 0.3, -0.25, 0.15, 0, 3.14, 0
placeVia = 0.3, -0.25, 0.15, 0, 3.14, 0
#picObject = 0.02, -0.400, 0.006, 0, 3.14, 0
placeObjectTabel2 = 0.3, -0.400, 0.03, 0, 3.14, 0
overPlaceObjectTabel2 = 0.3, -0.400, 0.1, 0, 3.14, 0
rob2PickConveyorA = -0.38, 0.3, 0.001, 2.24, 2.2, 0
rob2OverpicConveyorA = -0.38, 0.3, 0.1, 2.24, 2.2, 0
rob2OverPickPosTable = 0.02, -0.400, 0.1, 0.0, 3.14, 0.0


# function for moving robot using moveJ
def move(robot, location, moveWait):
    # moves robot
    robot.movex("movej", location, acc=a, vel=v, wait=moveWait, relative=False, threshold=None)
    if moveWait == False:
        time.sleep(0.1)


# Uses camera to locate objects
def locate_objects_rob():
    global x, y, objectLocated, switchCounter
    page = urllib.request.urlopen('http://10.1.1.8/CmdChannel?TRIG')
    time.sleep(2)
    page = urllib.request.urlopen('http://10.1.1.8/CmdChannel?gRES')
    # reads output from camera
    coords = page.read().decode('utf-8')
    # splits output
    x1 = coords.split(",")
    objectLocated = int(x1[2])
    if objectLocated == 1:
        switchCounter = 0
        y = x1[4]
        x = x1[3]
        x = (float(x) + 33) / 1000  # x = (float(x) + 25) /1000
        y = (float(y) - 350) / 1000  # y = (float(y) - 385) /1000  # 363
        time.sleep(3)
        print(x, y)

# pick object on table 1 rob1
def pick_object_from_table_rob1():
    global x, y, lastx, lasty, objectCount, placeObject, pickVia, placeConveyorA
    objectCount += 1
    lastx = x
    lasty = y
    overPickPos = x, y, 0.1, 0.0, 3.14, 0.0
    #overPickPos = 0.02, -0.400, 0.1, 0.0, 3.14, 0.0
    picObject = x, y, 0.018, 0, 3.14, 0
    # pickPos = x, y, 0.005, 0.0, 3.14, 0.0
    rob.send_program(rq_open())
    time.sleep(0.1)
    move(rob, overPickPos, True)
    move(rob, picObject, True)
    # closes gripper
    rob.send_program(rq_close())
    # sleep to allow gripper to close fully before program resumes
    time.sleep(0.6)
    move(rob, overPickPos, True)


# Local sorting on table 1
# to doo Test this function if working refactoring it, and implement for rob 2
def sort_on_table1():
    global x2, y2, x2i, y2i, objectCount, placeObject, pickVia, placeConveyorA
    if(objectCount<6): # 6
        print("objectount1.", objectCount)
        if(objectCount>1):
            x2 = x2 + float(0.0)
            y2 = y2 + float(0.09)
        else:
            pass
        overPickPos = 0.02, -0.400, 0.08, 0.0, 3.14, 0.0
        OvrPosplaceObject = -0.30-x2, -0.42+y2, 0.09, 0, 3.14, 0
        placeObject = -0.30-x2, -0.42+y2, 0.025, 0, 3.14, 0
        #move(rob, overPickPos, True)
        move(rob, OvrPosplaceObject, True)
        move(rob, placeObject, True)
        rob.send_program(rq_open())
        time.sleep(0.5)
        print(x2, y2)
        move(rob, clearCamera, True)
        #move(rob, overPickPos, True)
    else:
        if(objectCount>=6):
            x2i = x2i + float(0.0)  # Ned to give this variable a new indeviduale name in order to get it to work
            y2i = y2i + float(0.09)  # Same as x2 give its oven independent name form the  if above example x2i and y2i
            print("in second if else condition")
        else:
            pass
        overPickPos = 0.02, -0.400, 0.1, 0.0, 3.14, 0.0
        OverPosplaceObject = -0.30-x2i, -0.42+y2i, 0.2, 0, 3.14, 0
        placeObject = -0.30-x2i, -0.42+y2i, 0.07, 0, 3.14, 0
        #move(rob, overPickPos, True)
        move(rob, OverPosplaceObject, True)
        move(rob, placeObject, True)
        rob.send_program(rq_open())
        time.sleep(0.5)
        move(rob, OverPosplaceObject, True)
        print("cord it4", x2i, y2i)
        print("Test 4 runs")
        move(rob, clearCamera, True)
        #move(rob, overPickPos, True)


def program_complete():
    #stop_threads = True
    rob.close()
    rob2.close()
    print("program complete")
    #sys.exit()


# activates gripper. only needed once per power cycle
rob.send_program(rq_activate())
time.sleep(2.5)
rob2.send_program(rq_activate())
time.sleep(2.5)
# sets speed of gripper to max
rob.send_program(rq_set_speed(250))
time.sleep(0.1)
# sets force of gripper to a low value
rob.send_program(rq_set_force(10))
time.sleep(0.1)
# sets speed of gripper to max
rob2.send_program(rq_set_speed(250))
time.sleep(0.1)
# sets force of gripper to a low value
rob2.send_program(rq_set_force(10))
time.sleep(0.1)
# sets robot tcp, the distance from robot flange to gripper tips.
rob.set_tcp((0, 0, 0.16, 0, 0, 0))
rob2.set_tcp((0, 0, 0.16, 0, 0, 0))

# clear the robots away form the camera at the first
move(rob2, clearCamera, True)
move(rob, clearCamera, True)
#Setting the speed for the conveyer belt


def sorting_table1():
    while objectCount < 3:#6
        #locate_objects_rob2()
        locate_objects_rob()
        #-0.26 - x2i, -0.46 + y2i, 0.06, 0, 3.14, 0
        if (x != lastx or y != lasty) and (x != 0.025 or y != -0.385):
            pick_object_from_table_rob1()
            sort_on_table1()


print("rob1 finish sorting")

#sorting_table1()