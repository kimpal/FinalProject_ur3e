import urx
from Gripper import *
import urllib.request
import time

# set robot ip adress
# this is the left robot
r1 = "10.1.1.6"

# connects to robot
rob = urx.Robot(r1, use_rt=True, urFirm=5.1)

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
#placeObject = 0.3, -0.25, 0.15, 0, 3.14, 0
placeObject = 0.3, -0.25, 0.006, 0, 3.14, 0  # coordinate to please the block carefully on table
placeConveyorA = 0.2, 0.3, 0.005, 2.24, 2.2, 0
pickVia = 0.3, -0.25, 0.15, 0, 3.14, 0
placeVia = 0.3, -0.25, 0.15, 0, 3.14, 0
picObject = 0.02, -0.400, 0.006, 0, 3.14, 0


# function for moving robot using moveJ
def move(robot, location, moveWait):
    # moves robot
    robot.movex("movej", location, acc=a, vel=v, wait=moveWait, relative=False, threshold=None)
    if moveWait == False:
        time.sleep(0.1)


def pickObject():
    global x, y, lastx, lasty, objectCount, placeObject, pickVia, placeConveyorA
    objectCount += 1
    lastx = x
    lasty = y
    #overPickPos = x, y, 0.1, 0.0, 3.14, 0.0
    overPickPos = 0.02, -0.400, 0.1, 0.0, 3.14, 0.0
    #pickPos = x, y, 0.005, 0.0, 3.14, 0.0
    rob.send_program(rq_open())
    time.sleep(0.1)
    move(rob, overPickPos, True)
    #move(rob, pickPos, True)
    move(rob, picObject, True)
    # closes gripper
    rob.send_program(rq_close())
    # sleep to allow gripper to close fully before program resumes
    time.sleep(0.6)
    move(rob, overPickPos, True)
    #move(rob, placeObject, True)
    move(rob, placeVia, True)
    move(rob, placeConveyorA, True)
    rob.send_program(rq_open())
    time.sleep(0.2)
    move(rob, pickVia, True)


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
    #locateObjects()
    #if (x != lastx or y != lasty) and (x != 0.025 or y != -0.385):
        pickObject()
    #move(rob, clearCamera, True)

#while objectCount < 3:
#    locateObjects()
#    if x != lastx or y != lasty:
#        pickObject()

rob.close()