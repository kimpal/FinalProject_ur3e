import urx
from Gripper import *
import urllib.request
import time
# only Pseudokode code not working example
# some code that use the camera to sort object

plasePoss1 = False
plasePoss2 = False
a = 10
b = 5

def classifyObjec():
    if a > b:
        print("squereBloc")
        placeObject = 0.3, -0.25, 0.15, 0, 3.14, 0
    else:
        plasePoss2 == True
        print("Roundblock")

classifyObjec()

if plasePoss1 == True:
    # positions x, y, z, rx, ry, rz
    placeObject = 0.3, -0.25, 0.15, 0, 3.14, 0
else:
    print("dont Square Block")

if plasePoss2 == True:
    # positions x, y, z, rx, ry, rz
    placeObject = 0.9, -0.25, 0.15, 0, 3.14, 0
else:
    print("dont Round Block")

# set robot ip adress
# this is the left robot
r2 = "10.1.1.5"

# connects to robot
rob = urx.Robot(r2, use_rt=True, urFirm=5.1)


# function for moving robot using moveJ
def move(robot, location, moveWait):
    # moves robot
    robot.movex("movej", location, acc=a, vel=v, wait=moveWait, relative=False, threshold=None)
    if moveWait == False:
        time.sleep(0.1)


def plasePoss():
    global x, y, lastx, lasty, objectCount, placeObject
    overPickPos = x, y, 0.1, 0.0, 3.14, 0.0
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


    rob.close()