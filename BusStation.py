import os, sys
import subprocess
import pymysql
import time

def readNFC():
        strCom = "nfc-poll"
        print("NFC를 리더기에 읽어주세요")
        p = subprocess.Popen(strCom, stdout=subprocess.PIPE)
        p.poll()
        out = p.stdout.read()
        msg = out.decode('utf-8').split('(NFCID1): ')[1]
        id = msg.split('\n'[0])[0]
        return id

def selectUserNFC(cur):
        sql = "SELECT * FROM UserNFC"
        cur.execute(sql)
        res = cur.fetchall()
        return res

def selectBoardingInfo(cur):
        sql = "SELECT * FROM BoardingInfo"
        cur.execute(sql)
        res = cur.fetchall()
        return res

while True:
        busStation = '49122'
        sendID = readNFC()
        con = pymysql.connect(host = '192.168.0.37', user='Hari', password = '1234', db = 'BusInfo', charset = 'utf8')
        cur = con.cursor()
        res = selectUserNFC(cur)
        cnt = 0
        for data in res:
                if(sendID == data[0]):
                        cnt = cnt+1
                        break
                else:
                        continue
        if cnt == 0:
                print("등록되지 않은 사용자입니다.")
                continue

        print("탑승하실 버스 번호를 입력해 주세요: ")
        busNum = input();


        res = selectBoardingInfo(cur)
        for data in res:
                if (sendID == data[0]):
                        print("기존의 정보를 삭제하고 덮어씁니다.")
                        sql_b = "DELETE FROM BoardingInfo WHERE NFC_ID = %s"
                        cur.execute(sql_b,(sendID))
        sql = "INSERT INTO BoardingInfo (Bus, NFC_ID, BusStation) VALUES (%s, %s, %s)"
        cur.execute(sql,(busNum, sendID, busStation))
        con.commit()
        con.close()
        print("등록이 완료되었습니다.\n")