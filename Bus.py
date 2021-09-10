###Bus.py###
import time
import pymysql
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

line = ['49121', '49122', '49123', '49124', '49125','49126','49127','49128','49129','49130']
bus = '88'
location = 0


while True:
    user = 0
    buspos = line[location+1]
    con= pymysql.connect(host='192.168.0.37', user='190', password='1234', db='BusInfo', charset='utf8')
    cur = con.cursor()
    sql = "SELECT * FROM BoardingInfo"
    cur.execute(sql)
    res = cur.fetchall()

    for data in res:
        if((bus == data[1])&(buspos == data[2])):
            user = user + 1
            sql = "DELETE FROM BoardingInfo WHERE (Bus = %s AND BusStation = %s)"
            cur.execute(sql,(bus, buspos))
    if user != 0:
        print(user)
        print(buspos)
        GPIO.output(18, True)
    time.sleep(1)
    location = location+1
    GPIO.output(18, False)
    con.commit()
    con.close()
    if(location == len(line)-1):
        break
print(user)
