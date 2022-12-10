"""
This is the picking cylinders on table 2
and places them on the home area at table 2
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
# stop_threads = False
# robot_moving = True
# robot2_moving = True
# start_time = time.time()
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

# rob2 intitiating counter for object
x3 = 0
y3 = 0
x3i = 0
y3i = 0

# positions x, y, z, rx, ry, rz
clearCamera = 0.25, -0.22, 0.20, 0, 3.14, 0
# placeObject = 0.3, -0.25, 0.15, 0, 3.14, 0
placeObject = 0.3, -0.25, 0.03, 0, 3.14, 0  # coordinate to please the block carefully table 1
placeConveyorA = 0.2, 0.3, 0.0013, 2.24, 2.2, 0
overpickPlaceConveyorA = 0.2, 0.3, 0.1, 2.24, 2.2, 0
pickConveyorA = 0, 0.3, 0.15, 0, 3.14, 0
pickVia = 0.3, -0.25, 0.15, 0, 3.14, 0
placeVia = 0.3, -0.25, 0.15, 0, 3.14, 0
# picObject = 0.02, -0.400, 0.006, 0, 3.14, 0
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


# Uses camera to locate objects on rob2

def locate_objects_rob2():
    global x, y, objectLocated, switchCounter
    page = urllib.request.urlopen('http://10.1.1.7/CmdChannel?TRIG')
    time.sleep(2)
    page = urllib.request.urlopen('http://10.1.1.7/CmdChannel?gRES')
    # reads output from camera
    coords = page.read().decode('utf-8')
    # splits output
    x1 = coords.split(",")
    objectLocated = int(x1[2])
    if objectLocated == 1:
        switchCounter = 0
        y = x1[4]
        x = x1[3]
        x = (float(x) + 60) / 1000  # x = (float(x) + 25) /1000
        y = (float(y) - 375) / 1000  # y = (float(y) - 385) /1000  # 363
        time.sleep(3)
        print(x, y)


# pick object on table 2 rob2 # Working
def pick_object_from_table_rob2():
    global x, y, lastx, lasty, objectCount, placeObject, pickVia, placeConveyorA, clearCamera
    objectCount += 1
    lastx = x
    lasty = y
    overPickPos = x, y, 0.1, 0.0, 3.14, 0.0
    picObject = x, y, 0.015, 0, 3.14, 0
    rob2.send_program(rq_open())
    time.sleep(0.1)
    move(rob2, overPickPos, True)
    move(rob2, picObject, True)
    # closes gripper
    rob2.send_program(rq_close())
    # sleep to allow gripper to close fully before program resumes
    time.sleep(0.6)
    move(rob2, overPickPos, True)
    move(rob2, clearCamera, True)


def place_object_ontble2_incresed_yvalue():
    global x3, y3, x3i, y3i, lastx, lasty, objectCount, placeObjectTabel2, pickVia, placeConveyorA
    if (objectCount < 6):
        print("objectount1.", objectCount)
        if (objectCount > 1):
            x3 = x3 + float(0.0)
            y3 = y3 + float(0.09)
        else:
            pass
        placeObjectTabel2 = 0.3 + x3, -0.400 + y3, 0.018, 0, 3.14, 0
        overPlaceObjectTabel2 = 0.3 + x3, -0.400 + y3, 0.1, 0, 3.14, 0
        move(rob2, overPlaceObjectTabel2, True)
        move(rob2, placeObjectTabel2, True)
        rob2.send_program(rq_open())
        time.sleep(0.5)
        print(x3, y3)
        move(rob2, clearCamera, True)
    else:
        # x2 = -0.26
        # y2 = -0.46
        if (objectCount >= 5):
            x3i = x3i + float(0.0)
            y3i = y3i + float(0.09)
            print("in second if else condition")
        else:
            pass
        placeObjectTabel2 = 0.3 + x3i, -0.400 + y3i, 0.1, 0, 3.14, 0
        overPlaceObjectTabel2 = 0.3 + x3i, -0.400 + y3i, 0.2, 0, 3.14, 0
        move(rob2, overPlaceObjectTabel2, True)
        move(rob2, placeObjectTabel2, True)
        rob2.send_program(rq_open())
        time.sleep(0.5)
        move(rob2, overPlaceObjectTabel2, True)
        print("cord it4", x3i, y3i)
        print("Test 4 runs")
        move(rob2, clearCamera, True)


def program_complete():
    # stop_threads = True
    rob.close()
    rob2.close()
    print("program complete")
    # sys.exit()


# activates gripper. only needed once per power cycle
#rob2.send_program(rq_activate())
#time.sleep(2.5)
# sets speed of gripper to max
#rob2.send_program(rq_set_speed(250))
#time.sleep(0.1)
# sets force of gripper to a low value
#rob2.send_program(rq_set_force(10))
#time.sleep(0.1)
# sets robot tcp, the distance from robot flange to gripper tips.
#rob2.set_tcp((0, 0, 0.16, 0, 0, 0))

# clear the robots away form the camera at the first
move(rob2, clearCamera, True)


# sorting cylinders form tabel 2 to conveyer
def sortig_table2():
    while objectCount < 3:  # 6
        locate_objects_rob2()
        # -0.26 - x2i, -0.46 + y2i, 0.06, 0, 3.14, 0
        if (x != lastx or y != lasty) and (x != 0.025 or y != -0.385):
            pick_object_from_table_rob2()
            place_object_ontble2_incresed_yvalue()


print("Rob2 finish sorting")

# sortig_table2()
