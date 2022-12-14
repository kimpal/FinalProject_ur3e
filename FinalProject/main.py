"""
every code should be called form her to preform the whole task
"""
# pic and places on both robot simultaneously
import urx
import time
from threading import Thread
import sys
from Gripper import *
from blocsortingRob1 import sorting_table1
from blocksortingRob2 import sortig_table2
from rob1sendSylindertoRob2 import send_cylinders_to_table2
from rob2sendCubesToRob1 import send_cubes_to_table1


#set robot ip adresses
r1="10.1.1.6"
r2="10.1.1.5"

rob = urx.Robot(r1, use_rt=True, urFirm=5.1)
rob2 = urx.Robot(r2, use_rt=True, urFirm=5.1)

#robot velocity and acceleration
v = 0.8
a = 0.5
#variables
stop_threads = False
robMoving = True
rob2Moving = True
startTime = time.time()

clearCamera = 0.25, -0.22, 0.20, 0, 3.14, 0
handover1 = 0.55, -0.25, 0.45, 1.2, 1.2, 1.2
handover1b = 0.45, -0.25, 0.45, 1.2, 1.2, 1.2
handoverVia = 0.25, -0.22, 0.20, 0, 3.14, 0
handoverVia2 = -0.25, -0.22, 0.20, 0, 3.14, 0
handover2 = -0.48, -0.26, 0.455, 0, -1.57, 0
handover2b = -0.40, -0.26, 0.455, 0, -1.57, 0
placeObjectVia = -0.2, -0.3, 0.2, 0, 3.14, 0
pickConveyorA = 0, 0.3, 0.15, 0, 3.14, 0
pickConveyorVia = -0.3, 0, 0.15, 0, 3.14, 0
placeConveyor = 0.2, 0.3, 0.0, 2.24, 2.2, 0
placeConveyorA = 0.2, 0.3, 0.1, 2.24, 2.2, 0
placeConveyorVia = 0.3, -0.1, 0.1, 0, 3.14, 0


def move(robot, location, moveWait):
    robot.movex("movej", location, acc=a, vel=v, wait=moveWait, relative=False, threshold=None)
    if moveWait == False:
        time.sleep(0.1)


def program_complete():
    #global stop_threads
    stop_threads = True
    rob.close()
    rob2.close()
    print("program complete")
    sys.exit()


def moverob():
    while 1:
        if stop_threads:
            break
        sorting_table1()


def moverob2():
    while 1:
        if stop_threads:
            break
        sortig_table2()


rob.send_program(rq_activate())
time.sleep(2.5)
rob2.send_program(rq_activate())
time.sleep(2.5)
rob.send_program(rq_set_speed(250))
time.sleep(0.1)
rob.send_program(rq_set_force(10))
time.sleep(0.1)
rob2.send_program(rq_set_speed(250))
time.sleep(0.1)
rob2.send_program(rq_set_force(10))
time.sleep(0.1)
rob.set_tcp((0,0,0.16,0,0,0))
rob2.set_tcp((0,0,0.16,0,0,0))

#this is the secvense the coe is executed in
Thread(target = moverob).start()
Thread(target = moverob2).start()
print("heisan hoppsan(starting the sorting)")
#send_cylinders_to_table2()
#send_cubes_to_table1()

time.sleep(96) # try whit 96
print("start sending objects")
send_cylinders_to_table2()
time.sleep(30)
send_cubes_to_table1()
time.sleep(30)
program_complete()
