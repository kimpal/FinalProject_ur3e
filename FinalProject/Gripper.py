import inspect

####Single command example usage####
#rob.send_program(rq_close())

def rq_reset():
    return open("Gripper.script", "rb").read().decode("utf-8") + "  " + inspect.stack()[0][3] + "()\nend"
    
def rq_activate_and_wait():
    return open("Gripper.script", "rb").read().decode("utf-8") + "  " + inspect.stack()[0][3] + "()\nend"
    
def rq_activate():
    return open("Gripper.script", "rb").read().decode("utf-8") + "  " + inspect.stack()[0][3] + "()\nend"
    
def rq_close():
    return open("Gripper.script", "rb").read().decode("utf-8") + "  " + inspect.stack()[0][3] + "()\nend"
    
def rq_close_and_wait():
    return open("Gripper.script", "rb").read().decode("utf-8") + "  " + inspect.stack()[0][3] + "()\nend"
    
def rq_open():
    return open("Gripper.script", "rb").read().decode("utf-8") + "  " + inspect.stack()[0][3] + "()\nend"
    
def rq_open_and_wait():
    return open("Gripper.script", "rb").read().decode("utf-8") + "  " + inspect.stack()[0][3] + "()\nend"
    
def rq_is_object_detected():
    return open("Gripper.script", "rb").read().decode("utf-8") + "  " + inspect.stack()[0][3] + "()\nend"

def rq_move(number):
    return open("Gripper.script", "rb").read().decode("utf-8") + "  " + inspect.stack()[0][3] + "(" + str(number) + ")\nend"
    
def rq_set_force(number):
    return open("Gripper.script", "rb").read().decode("utf-8") + "  " + inspect.stack()[0][3] + "(" + str(number) + ")\nend"
    
def rq_set_speed(number):
    return open("Gripper.script", "rb").read().decode("utf-8") + "  " + inspect.stack()[0][3] + "(" + str(number) + ")\nend"
       
####Multiple commands example usage####
#commands = ["rq_open", "rq_close"]
#rob.send_program(rq_multiple_commands(commands))
def rq_multiple_commands(commands):
    l = open("Gripper.script", "rb").read().decode("utf-8")
    for command in commands:
        if (command in globals()):
            l += "  " + command +"()\n"
        else:
            return command
    l += "end"
    return l