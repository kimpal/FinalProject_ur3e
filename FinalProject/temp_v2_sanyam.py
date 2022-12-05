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

# positions x, y, z, rx, ry, rz
clearCamera = 0.25, -0.22, 0.20, 0, 3.14, 0
# placeObject = 0.3, -0.25, 0.15, 0, 3.14, 0
placeObject = 0.3, -0.25, 0.03, 0, 3.14, 0  # coordinate to please the block carefully table 1
placeConveyorA = 0.2, 0.3, 0.005, 2.24, 2.2, 0
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

''''
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
'''


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
        x = (float(x) + 40) / 1000  # x = (float(x) + 25) /1000
        y = (float(y) - 385) / 1000  # y = (float(y) - 385) /1000  # 363
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
    picObject = x, y, 0.006, 0, 3.14, 0
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


def place_object_on_conveyer_rob1():
    global x, y, lastx, lasty, objectCount, placeObject, pickVia, placeConveyorA, overpickPlaceConveyorA
    #objectCount += 1
    lastx = x
    lasty = y
    move(rob, placeVia, True)
    move(rob, overpickPlaceConveyorA, True)
    move(rob, placeConveyorA, True)
    rob.send_program(rq_open())
    time.sleep(0.5)
    move(rob, pickVia, True)


# function to pic object form the conveyer on rob1
def pick_object_on_conveyer_rob1():
    global x, y, lastx, lasty, objectCount, placeObject, pickVia, placeConveyorA, overpickPlaceConveyorA
    #objectCount += 1
    lastx = x
    lasty = y
    rob.send_program(rq_open())
    time.sleep(0.2)
    move(rob, overpickPlaceConveyorA, True)
    move(rob, placeConveyorA, True)# nead to fix
    time.sleep(0.9)
    rob.send_program(rq_close())
    time.sleep(0.9)
    move(rob, overpickPlaceConveyorA, True)
    move(rob, pickVia, True)

#counter = 0
#for i in range(number_of_objects):
#    if(counter<=number_of_objects):
#        increase(x,y)
#        x = x + some_significant_value
#        y = y + some_significant_value
#    else:
#        pass
#your_functions(x,y)

# Testing whit increased y  work need also to increase x value after 4 rounds
# to place it in a nice order
def place_object_on_table_rob1():
    global x2, y2, lastx, lasty, objectCount, placeObject, pickVia, placeConveyorA
    #objectCount += 1
    #x2 = 0
    #y2 = 0
    if(objectCount<4):
        if(objectCount>1):
            x2 = x2 + float(0.0)
            y2 = y2 + float(0.09)
        else:
            pass
        #lastx = x
        #lasty = y
        overPickPos = 0.02, -0.400, 0.1, 0.0, 3.14, 0.0
        placeObject = -0.26-x2, -0.46+y2, 0.03, 0, 3.14, 0
        #move(rob, overPickPos, True)
        move(rob, placeObject, True)
        rob.send_program(rq_open())
        time.sleep(0.5)
        print(x2, y2)
        move(rob, clearCamera, True)
        #move(rob, overPickPos, True)
    else:
        if(objectCount>=4):
            x2 = x2 + float(0.0)
            y2 = y2 + float(0.09)
        else:
            pass
        #lastx = x
        #lasty = y
        overPickPos = 0.02, -0.400, 0.1, 0.0, 3.14, 0.0
        placeObject = -0.26-x2, -0.46+y2, 0.03, 0, 3.14, 0
        #move(rob, overPickPos, True)
        move(rob, placeObject, True)
        rob.send_program(rq_open())
        time.sleep(0.5)
        print(x2, y2)
        move(rob, clearCamera, True)
        #move(rob, overPickPos, True)


# pick object on table 2 rob2 # Working
def pick_object_from_table_rob2():
    global x, y, lastx, lasty, objectCount, placeObject, pickVia, placeConveyorA, clearCamera
    objectCount += 1
    lastx = x
    lasty = y
    #overPickPos = X, y, 0.1, 0.0, 3.14, 0.0
    #picObject = X, y, 0.006, 0, 3.14, 0
    overPickPos = x, y, 0.1, 0.0, 3.14, 0.0
    picObject = x, y, 0.006, 0, 3.14, 0
    #overPickPos = 0.02, -0.400, 0.1, 0.0, 3.14, 0.0
    #picObject = 0.02, -0.400, 0.006, 0, 3.14, 0
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


def place_object_on_tabl_rob2():
    global x, y, lastx, lasty, objectCount, table2PositionCount, placeObject, pickVia, placeConveyorA
    #objectCount += 1
    # Nead to figure out how to imcrease plase postion for each placing so next object get new pos
    table2PositionCount += 10
    yNew = 0.3 + table2PositionCount
    #overPickPos = X, y, 0.1, 0.0, 3.14, 0.0
    #picObject = X, y, 0.006, 0, 3.14, 0
    #placeObjectTabel2 = 0.3, -0.400, 0.03, 0, 3.14, 0
    #overPlaceObjectTabel2 = 0.3, -0.400, 0.1, 0, 3.14, 0
    #overPickPos = 0.02, -0.400, 0.1, 0.0, 3.14, 0.0
    #picObject = 0.02, -0.400, 0.006, 0, 3.14, 0
    #time.sleep(0.1)
    #move(rob2, picObject, True)
    #rob2.send_program(rq_open())
    #move(rob2, rob2OverPickPosTable, True)  # position over the table
    move(rob2, overPlaceObjectTabel2, True)
    move(rob2, placeObjectTabel2, True)
    rob2.send_program(rq_open())
    time.sleep(0.9)
    move(rob2, overPlaceObjectTabel2, True)
    move(rob2, clearCamera, True)


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


# function to pic object on conveyer from rob2
def pick_object_on_conveyer_rob2():
    global x, y, lastx, lasty, objectCount, placeObject, pickVia, rob2OverpicConveyorA, rob2OverPickPosTable, rob2PickConveyorA, picObject, placeObjectTabel2
    #objectCount += 1
    lastx = x
    lasty = y
    move(rob2, clearCamera, True)
    rob2.send_program(rq_open())
    time.sleep(0.1)
    move(rob2, clearCamera, True)
    move(rob2, rob2OverpicConveyorA, True)
    move(rob2, rob2PickConveyorA, True)
    time.sleep(0.9)
    rob2.send_program(rq_close())
    time.sleep(0.9)
    move(rob2, rob2OverpicConveyorA, True)
    time.sleep(0.1)
    move(rob2, clearCamera, True)
    # Need to add and via position as for rob 1
    # move(rob2, rob2OverPickPosTable, True) # position over the table
    # move(rob2, placeObjectTabel2, True)
    # rob2.send_program(rq_open())


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
move(rob, clearCamera, True)
#Setting the speed for the conveyer belt
set_conveyor_speed(0.400)


def move_detected_object_to_conveyor_rob1():
    pick_object_from_table_rob1()
    place_object_on_conveyer_rob1()
    start_conveyor()
    time.sleep(3.6)  # this tim is perfect with the speed to get the object in good position for pic form rob2
    stop_conveyor()


def move_object_form_conveyer_rob2_to_tabel():
    pick_object_on_conveyer_rob2()
    place_object_on_tabl_rob2()


def move_detected_object_to_conveyor_rob2():
    pick_object_from_table_rob2()
    place_object_on_conveyer_rob2()
    reverse_conveyor()
    time.sleep(3.6)
    stop_conveyor()


def move_object_form_conveyor_rob1_to_table():
    pick_object_on_conveyer_rob1()
    place_object_on_table_rob1()

#while objectCount < 1:
    #locateObjects()
    #if (x != lastx or y != lasty) and (x != 0.025 or y != -0.385):
        #pickObject()

        # This code part is tested and work as intended
        # portion of the code to pic object form table 1 and place it on the conveyer
        # and start it and pic the objct vit rob2
        #pick_object_from_table_rob1()
        #place_object_on_conveyer_rob1()
        #start_conveyor()
        #time.sleep(3.6)  # this tim is perfect with the speed to get the object in good position for pic form rob2
        #stop_conveyor()
        #pick_object_on_conveyer_rob2()
        #place_object_on_tabl_rob2()

        # The steps below is working as intended!
        # This part of the code pic object form table 2 and places it on the conveyer
        # Then rob 1 pics it up and sets int at the table
        #pick_object_from_table_rob2()
        #place_object_on_conveyer_rob2()
        #reverse_conveyor()
        #time.sleep(3.6)  # this tim is perfect with the speed to get the object in good position for pic form rob2
        #stop_conveyor()
        #pick_object_on_conveyer_rob1()
        #place_object_on_table_rob1()


# sorting cylinders form tabel 1 to conveyer
while objectCount < 4:
    locate_objects_rob2()
    # locate_objects_rob()
    if (x != lastx or y != lasty) and (x != 0.025 or y != -0.385):
        #move_detected_object_to_conveyor_rob1()
        #move_object_form_conveyer_rob2_to_tabel()
        move_detected_object_to_conveyor_rob2()
        move_object_form_conveyor_rob1_to_table()
#rob.close()
#rob2.close()
program_complete()
