import urx
from Gripper import *
import urllib.request
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

# positions x, y, z, rx, ry, rz
clearCamera = 0.25, -0.22, 0.20, 0, 3.14, 0
# placeObject = 0.3, -0.25, 0.15, 0, 3.14, 0
placeObject = 0.3, -0.25, 0.006, 0, 3.14, 0  # coordinate to please the block carefully
placeConveyorA = 0.2, 0.3, 0.005, 2.24, 2.2, 0
overpickPlaceConveyorA = 0.2, 0.3, 0.1, 2.24, 2.2, 0
pickConveyorA = 0, 0.3, 0.15, 0, 3.14, 0
pickVia = 0.3, -0.25, 0.15, 0, 3.14, 0
placeVia = 0.3, -0.25, 0.15, 0, 3.14, 0
picObject = 0.02, -0.400, 0.006, 0, 3.14, 0
rob2PickConveyorA = -0.38, 0.3, 0.001, 2.24, 2.2,
rob2OverpicConveyorA = -0.38, 0.3, 0.1, 2.24, 2.2,
rob2OverPickPosTable = 0.02, -0.400, 0.1, 0.0, 3.14, 0.0


# function for moving robot using moveJ
def move(robot, location, moveWait):
    # moves robot
    robot.movex("movej", location, acc=a, vel=v, wait=moveWait, relative=False, threshold=None)
    if moveWait == False:
        time.sleep(0.1)

'''''
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
        x = (float(x) + 25) / 1000  # x = (float(x) + 25) /1000
        y = (float(y) - 385) / 1000  # y = (float(y) - 385) /1000  # 363
        time.sleep(3)
        print(x, y)
'''

# Moves robot to coordinates set by camera
#function for rob1
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
    move(rob, placeVia, True)
    #move(rob, placeObject, True)
    move(rob, placeConveyorA, True)
    rob.send_program(rq_open())
    time.sleep(0.2)
    move(rob, pickVia, True)
    #time.sleep(0.1)
    #startConveyor()
    #time.sleep(3)
    #stopConveyor()


# Need to fix this function for the robot 2
# this is just a test function to figure out the cordiant and that
def pickObjectRob2():
    global x, y, lastx, lasty, objectCount, placeObject, pickVia, placeConveyorA
    objectCount += 1
    lastx = x
    lasty = y
    # positions x, y, z, rx, ry, rz
    #starther = -0.2, -0.3, 0.1, 0.0, 3.14, 0.0  # need to figure out the position
    #overPickPos = -0.4, -0.5, 0.1, 0.0, 3.14, 0.0  # Need to figure out the positions
    overPickPos = 0.02, -0.400, 0.2, 0.0, 3.14, 0.0
    picObject = 0.02, -0.400, 0.006, 0, 3.14, 0
    pickConveyorA2 = -0.38, 0.3, 0.005, 2.24, 2.2, 0
    overplaceConveyorA2 = -0.38, 0.3, 0.1, 2.24, 2.2, 0
    placeConveyorA2 = -0.38, 0.3, 0.005, 2.24, 2.2, 0
    move(rob2, overPickPos, True)
    rob2.send_program(rq_open())
    time.sleep(0.1)
    move(rob2, picObject, True)
    # closes gripper
    rob2.send_program(rq_close())
    # sleep to allow gripper to close fully before program resumes
    time.sleep(0.6)
    move(rob2, overPickPos, True)
    move(rob2, overplaceConveyorA2, True)
    time.sleep(0.1)
    move(rob2, placeConveyorA2, True)
    rob2.send_program(rq_open())
    time.sleep(0.6)
    rob2.send_program(rq_close())
    move(rob2, overplaceConveyorA2, True)

    #move(rob2, via, True)
    #move(rob, placeObjectAtTable, True)
    #rob2.send_program(rq_open())
    #time.sleep(0.2)
    #move(rob2, via, True

# pick object on table 1 rob
def pickObjectFromTableRob1():
    global x, y, lastx, lasty, objectCount, placeObject, pickVia, placeConveyorA
    objectCount += 1
    lastx = x
    lasty = y
    # overPickPos = x, y, 0.1, 0.0, 3.14, 0.0
    #overPickPos = x, y, 0.1, 0.0, 3.14, 0.0
    overPickPos = 0.02, -0.400, 0.1, 0.0, 3.14, 0.0
    #picObject = x, y, 0.006, 0, 3.14, 0
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


# function to pic object form the conveyer on rob1
def pickobjectOnconveryerRob1():
    global x, y, lastx, lasty, objectCount, placeObject, pickVia, placeConveyorA, overpickPlaceConveyorA
    objectCount += 1
    lastx = x
    lasty = y
    move(rob, overpickPlaceConveyorA, True)
    move(rob, placeConveyorA, True)
    rob.send_program(rq_open())
    time.sleep(0.9)
    rob.send_program(rq_close())
    time.sleep(0.9)
    move(rob, overpickPlaceConveyorA, True)
    move(rob, pickVia, True)

# pick object on table 2 rob2
def picObjecFromTableRob2():
    global x, y, lastx, lasty, objectCount, placeObject, pickVia, placeConveyorA
    objectCount += 1
    lastx = x
    lasty = y
    #overPickPos = X, y, 0.1, 0.0, 3.14, 0.0
    #picObject = X, y, 0.006, 0, 3.14, 0
    overPickPos = 0.02, -0.400, 0.1, 0.0, 3.14, 0.0
    picObject = 0.02, -0.400, 0.006, 0, 3.14, 0
    move(rob2, overPickPos, True)
    rob2.send_program(rq_open())
    time.sleep(0.1)
    move(rob2, picObject, True)
    # closes gripper
    rob2.send_program(rq_close())
    # sleep to allow gripper to close fully before program resumes
    time.sleep(0.6)
    move(rob2, overPickPos, True)



# function to pic object on conveyer from rob2
def pickobjecOnConveyerRob2():
    global x, y, lastx, lasty, objectCount, placeObject, pickVia, rob2OverpicConveyorA, rob2OverPickPosTable
    objectCount += 1
    lastx = x
    lasty = y
    rob2.send_program(rq_open())
    time.sleep(0.1)
    move(rob2, rob2OverpicConveyorA, True)
    move(rob2, rob2PickConveyorA, True)
    time.sleep(0.9)
    rob2.send_program(rq_close())
    time.sleep(0.9)
    move(rob2, rob2OverpicConveyorA, True)
    time.sleep(0.1)
    #Nead to add an via postion as for rob 1
    move(rob2, rob2OverPickPosTable, True) # position over the table



#Conveyour is the code that controlls te conveyer belt
def startConveyor():
    #start coveyor
    rob2.set_digital_out(5, 1)
    #allow digital out 5 to stay active for 0.1s
    time.sleep(0.1)
    #set digital out back to 0
    rob2.set_digital_out(5, 0)
    #conveyor started

def stopConveyor():
    #stop conveyor
    rob2.set_digital_out(7, 1)
    #allow digital out 7 to stay active for 0.1s
    time.sleep(0.1)
    #set digital out back to 0
    rob2.set_digital_out(7, 0)
    #conveyor stopped

def reverseConveyor():
    #start coveyor in reverse direction
    rob2.set_digital_out(6, 1)
    #allow digital out 6 to stay active for 0.1s
    time.sleep(0.1)
    #set digital out back to 0
    rob2.set_digital_out(6, 0)
    #conveyor started in reverse direction


def setConveyorSpeed(voltage):
    #sets analog out to voltage instead of current
    rob2.send_program("set_analog_outputdomain(1, 1)")
    #sets analog out 1 to desired voltage. 0.012 is the slowest speed.
    rob2.set_analog_out(1, voltage)

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

move(rob, clearCamera, True)



move(rob, clearCamera, True)
#Setting the speed for the conveyer blt
setConveyorSpeed(0.400)

while objectCount < 1:
    #locateObjects()
    #if (x != lastx or y != lasty) and (x != 0.025 or y != -0.385):
        pickObject()
        startConveyor()
        time.sleep(4.0)  # this tim is perfect with the speed to get the object in good position for pic form rob2
        stopConveyor()
        #pickobjecOnConveyerRob2()
        pickObjectRob2()
        #pickobjecOnConveyerRob2()


    #move(rob, clearCamera, True)

#while objectCount < 3:
#    locateObjects()
#    if x != lastx or y != lasty:
#        pickObject()

rob.close()
rob2.close()
