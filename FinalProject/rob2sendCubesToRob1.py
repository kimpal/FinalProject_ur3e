"""
This is the code that pic object on table 2 and places it on the conveyorbelt
and send it to robot1 that pleases the object in the home area at table 1
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
#picObject = 0.02, -0.400, 0.006, 0, 3.14, 0
placeObjectTabel2 = 0.3, -0.400, 0.03, 0, 3.14, 0
overPlaceObjectTabel2 = 0.3, -0.400, 0.1, 0, 3.14, 0
rob2PickConveyorA = -0.38, 0.3, 0.0001, 2.24, 2.2, 0
rob2OverpicConveyorA = -0.38, 0.3, 0.1, 2.24, 2.2, 0
rob2OverPickPosTable = 0.02, -0.400, 0.1, 0.0, 3.14, 0.0


# function for moving robot using moveJ
def move(robot, location, moveWait):
    # moves robot
    robot.movex("movej", location, acc=a, vel=v, wait=moveWait, relative=False, threshold=None)
    if moveWait == False:
        time.sleep(0.1)

#use camera to detect object
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


# Keep it
# function to pic object form the conveyer on rob1
def pick_object_on_conveyer_rob1():
    global x, y, objectCount, placeObject, pickVia, placeConveyorA, overpickPlaceConveyorA
    rob.send_program(rq_open())
    time.sleep(0.2)
    move(rob, overpickPlaceConveyorA, True)
    move(rob, placeConveyorA, True)# nead to fix
    time.sleep(0.9)
    rob.send_program(rq_close())
    time.sleep(0.9)
    move(rob, overpickPlaceConveyorA, True)
    move(rob, pickVia, True)


# Testing whit increased y  work need also to increase x value after 4 rounds
# to place it in a nice order
def place_object_on_table_rob1():
    global x2, y2, objectCount, placeObject, pickVia, placeConveyorA
    if(objectCount>1):
        x2 = x2 + float(0.0)
        y2 = y2 + float(0.09)
    else:
        pass
    overPickPos = 0.02, -0.400, 0.1, 0.0, 3.14, 0.0
    placeObject = -0.26-x2, -0.46+y2, 0.03, 0, 3.14, 0
    #move(rob, overPickPos, True)
    move(rob, placeObject, True)
    rob.send_program(rq_open())
    time.sleep(0.5)
    print(x2, y2)
    move(rob, clearCamera, True)
    #move(rob, overPickPos, True)


# pick object on table2 rob2
def pick_object_from_table_rob2():
    global x, y, lastx, lasty, objectCount, placeObject, pickVia, placeConveyorA, clearCamera
    objectCount += 1
    lastx = x
    lasty = y
    overPickPos = x, y, 0.1, 0.0, 3.14, 0.0
    picObject = x, y, 0.006, 0, 3.14, 0
    rob2.send_program(rq_open())
    time.sleep(0.1)
    move(rob2, overPickPos, True)
    move(rob2, picObject, True)
    # closes gripper
    rob2.send_program(rq_close())
    # sleep to allow gripper to close fully before program resumes
    time.sleep(0.6)
    move(rob2, overPickPos, True)
    #move(rob2, clearCamera, True)


# kep this
# command to place object on conveyer need to be run after the pic command form the table
def place_object_on_conveyer_rob2():
    global x, y, lastx, lasty, objectCount, placeObject, pickVia, rob2OverpicConveyorA, rob2OverPickPosTable, rob2PickConveyorA, picObject, placeObjectTabel2
    #objectCount += 1
    lastx = x
    lasty = y
    move(rob2, rob2OverpicConveyorA, True)
    move(rob2, rob2PickConveyorA, True)
    time.sleep(0.1)
    rob2.send_program(rq_open())
    time.sleep(0.9)
    move(rob2, rob2OverpicConveyorA, True)
    move(rob2, clearCamera, True)


# Conveyor is the code that controls te conveyer belt
def start_conveyor():
    # start coveyor
    rob2.set_digital_out(5, 1)
    # allow digital out 5 to stay active for 0.1s
    time.sleep(0.1)
    # set digital out back to 0
    rob2.set_digital_out(5, 0)
    # conveyor started


def stop_conveyor():
    # stop conveyor
    rob2.set_digital_out(7, 1)
    # allow digital out 7 to stay active for 0.1s
    time.sleep(0.1)
    # set digital out back to 0
    rob2.set_digital_out(7, 0)
    # conveyor stopped


def reverse_conveyor():
    # start conveyor in reverse direction
    rob2.set_digital_out(6, 1)
    # allow digital out 6 to stay active for 0.1s
    time.sleep(0.1)
    # set digital out back to 0
    rob2.set_digital_out(6, 0)
    # conveyor started in reverse direction


def set_conveyor_speed(voltage):
    # sets analog out to voltage instead of current
    rob2.send_program("set_analog_outputdomain(1, 1)")
    # sets analog out 1 to desired voltage. 0.012 is the slowest speed.
    rob2.set_analog_out(1, voltage)


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
#Setting the speed for the conveyer belt
set_conveyor_speed(0.400)


def move_detected_object_to_conveyor_rob2():
    pick_object_from_table_rob2()
    place_object_on_conveyer_rob2()
    reverse_conveyor()
    time.sleep(3.3) # tested and perfect sleep time before conveyor stops
    stop_conveyor()


def move_object_form_conveyor_rob1_to_table():
    pick_object_on_conveyer_rob1()
    place_object_on_table_rob1()


# pickong cubes form tabel 2 and sends it to tabl1 home area
def send_cubes_to_table1():
    while objectCount < 3:
        locate_objects_rob2()
        if (x != lastx or y != lasty) and (x != 0.025 or y != -0.385):
            move_detected_object_to_conveyor_rob2() #use to runn the rob 2 send to rob 1 code file
            move_object_form_conveyor_rob1_to_table() #use to runn the rob 2 sedn to rob 1 code fiel


#send_cubes_to_table1()
#program_complete()
print("completed sending object to table 2")
