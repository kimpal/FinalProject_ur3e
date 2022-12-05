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
