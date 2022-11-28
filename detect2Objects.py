import urx
import urllib.request
import time

x = float(25/1000)
y = float(-385/1000)
lasty = y
lastx = x
objectLocated = 0
whichObject = 0
switchCounter = 0


def locateObjects():
    global x, y, objectLocated, whichObject, switchCounter
    page = urllib.request.urlopen('http://10.1.1.8/CmdChannel?TRIG')
    time.sleep(2)
    page = urllib.request.urlopen('http://10.1.1.8/CmdChannel?gRES')
    #reads output from camera
    coords = page.read().decode('utf-8')
    #splits output
    x1 = coords.split(",")
    whichObject = int(x1[1])
    objectLocated = int(x1[2])
    if objectLocated == 1:
        switchCounter = 0
        y = x1[4]
        x = x1[3]
        x = (float(x) + 25) / 1000
        y = (float(y) - 385) / 1000
        time.sleep(3)
        print(x, y)
        locateObjects()
    
  
def switchObject():
    global whichObject, switchCounter
    switchCounter += 1
    if whichObject == 0:
        page = urllib.request.urlopen('http://10.1.1.8/CmdChannel?sINT_1_1')
        time.sleep(3)
    if whichObject == 1:
        page = urllib.request.urlopen('http://10.1.1.8/CmdChannel?sINT_1_0')
        time.sleep(3)
    time.sleep(1)
    print("object switched")
    
    
while switchCounter < 3:
    locateObjects()
    switchObject()