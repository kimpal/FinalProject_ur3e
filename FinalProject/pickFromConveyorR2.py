import urx
from Gripper import *
from conveyorR2 import *
import urllib.request
import time

# set robot ip adress
# this is the left robot
r2 = "10.1.1.5"

# connects to robot
rob = urx.Robot(r2, use_rt=True, urFirm=5.1)

# robot velocity and acceleration
v = 0.8
a = 0.5
# variables
# these x and y values are the distance from the robot base to the middle of the camera
x = float(25 / 1000)
y = float(-385 / 1000)
lasty = y
lastx = x
objectLocated = 0
objectCount = 0

# positions x, y, z, rx, ry, rz
clearCamera = 0.25, -0.22, 0.20, 0, 3.14, 0
placeObject = 0.3, -0.25, 0.15, 0, 3.14, 0
pickConveyorA = 0, 0.3, 0.15, 0, 3.14, 0
pickConveyorVia = -0.3, 0, 0.15, 0, 3.14, 0


# function for moving robot using moveJ
def move(robot, location, moveWait):
    # moves robot
    robot.movex("movej", location, acc=a, vel=v, wait=moveWait, relative=False, threshold=None)
    if moveWait == False:
        time.sleep(0.1)

##Nead a code to pic the object form the conveyor


# Uses camera to locate objects
def locateObjects():
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
        x = (float(x) + 25) / 1000
        y = (float(y) - 385) / 1000
        time.sleep(3)
        print(x, y)


# Moves robot to coordinates set by camera
def pickObject():
    global x, y, lastx, lasty, objectCount, placeObject
    objectCount += 1
    lastx = x
    lasty = y
    overPickPos = x, y, 0.1, 0.0, 3.14, 0.0
    pickPos = x, y, 0.005, 0.0, 3.14, 0.0
    rob.send_program(rq_open())
    time.sleep(0.1)
    move(rob, overPickPos, True)
    move(rob, pickPos, True)
    # closes gripper
    rob.send_program(rq_close())
    # sleep to allow gripper to close fully before program resumes
    time.sleep(0.6)
    move(rob, overPickPos, True)
    move(rob, placeObject, True)
    rob.send_program(rq_open())
    time.sleep(0.2)


# activates gripper. only needed once per power cycle
rob.send_program(rq_activate())
time.sleep(2.5)
# sets speed of gripper to max
rob.send_program(rq_set_speed(250))
time.sleep(0.1)
# sets force of gripper to a low value
rob.send_program(rq_set_force(10))
time.sleep(0.1)
# sets robot tcp, the distance from robot flange to gripper tips.
rob.set_tcp((0, 0, 0.16, 0, 0, 0))

move(rob, clearCamera, True)

while objectCount < 3:
    locateObjects()
    if (x != lastx or y != lasty) and (x != 0.025 or y != -0.385):
        pickObject()

rob.close()