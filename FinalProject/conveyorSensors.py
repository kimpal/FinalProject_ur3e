import requests

#change port[n] to change sensor. 1 is closest to the door, 4 is furthest away from the door
r = requests.post('http://10.1.1.9', json={"code":"request","cid":1,"adr":"/getdatamulti","data":{"datatosend":["/iolinkmaster/port[1]/iolinkdevice/pdin"]}})

res = r.json()

res1 = res['data']

data = str(res1)
print(res)

if data[53] == "2":
    d = data[68]+data[69]
    p = int(d,16)
else:
    p = ("out of range")
    
print(p)