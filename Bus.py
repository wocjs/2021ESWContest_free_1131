import time
import pymysql
import RPi.GPIO as GPIO

line = ['49121' '49122', '49123', '49124', '49125','49126','49127','49128','49129','49130']
bus = '88'
location = 0
#GPIO Initialize
def initGPIO():
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.OUT)
        GPIO.setup(17, GPIO.OUT)
        GPIO.output(17, False)
        GPIO.output(18, False)
#Read From DataBase
def inquiryDB(user):
        sql = "SELECT * FROM BoardingInfo"
        cur.execute(sql)
        res = cur.fetchall()

        for data in res:
                if((bus == data[1])&(buspos == data[2])):
                        user = user + 1
                        sql = "DELETE FROM BoardingInfo WHERE (Bus = %s AND BusStation = %s)"
                        cur.execute(sql,(bus, buspos))
        ctlLED(user)
        return user
#LED Controller
def ctlLED(passenger):
        if passenger == 0:
                GPIO.output(18, True)
        else:
                GPIO.output(18, False)

#Normal Operation Display
initGPIO()

while True:

        user = 0
        con = pymysql.connect(host='192.168.1.202', user='190', password='1234', db='BusInfo', charset='utf8')
        cur = con.cursor()
        buspos = line[location+1]
        user = inquiryDB(user)

        print("User = ", user)
        print("BusPosition = ", buspos)

        time.sleep(1)
        location = location + 1

        con.commit()
        con.close()
        if(location == (len(line)-1)):
                break
#Operation End
GPIO.output(17, True)
GPIO.cleanup()