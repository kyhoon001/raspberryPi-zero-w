from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtSql
#to sensehat
from sense_hat import SenseHat
from time import sleep

#to seconds
import re


class pollingThread(QThread):
  
  mh = Raspi_MotorHAT(0x6f)
    
  #servomotor setting
  servo = mh._pwm
  servo.setPWMFreq(60)
  s_middle = 350
  s_left = 215
  s_right = 430
    
  #dcmotor setting
  dcMotor = mh.getMotor(1)
  dcMotor.setSpeed(125)
  servo.setPWM(0,0,s_middle)
  
  #sense_hat
  sense = SenseHat()

  def init(self):
    super().init()
    
    
  def run(self):
    self.db = QtSql.QSqlDatabase.addDatabase('QMYSQL')
    self.db.setHostName("3.34.124.67")
    self.db.setDatabaseName("16_9")
    self.db.setUserName("16_9")
    self.db.setPassword("1234")
    ok = self.db.open()
    print(ok)
    
    
    while True:
      #time.sleep(0.1)
      sleep(0.1)
      self.getQuery() #get command
      self.setQuery()


  ######################## about the sensehat data
  def setQuery(self):
    pressure = self.sense.get_pressure()
    temp = self.sense.get_temperature()
    humidity = self.sense.get_humidity()
    
    p = round((pressure - 1000) / 10 , 2)
    if p > 1 :
      p = 1
    t = round(temp / 100, 2)
    h = round(humidity / 100,2)
    
    #for debug
    #msg = "Press : " + str(p) + "   Temp : " + str(t) + "   Humid : " + str(h)
    #print(msg)
    #sleep(0.01)
    
    
    
    #to mysql - DB Part
    self.query = QtSql.QSqlQuery();
    self.query.prepare("insert into sensing1 (time, num1, num2, num3, meta_string, is_finish) values(:time, :num1, :num2, :num3, :meta, :finish)");
    
    time = QDateTime().currentDateTime()
    self.query.bindValue(":time", time)
    self.query.bindValue(":num1", p)
    self.query.bindValue(":num2", t)
    self.query.bindValue(":num3", h)
    self.query.bindValue(":meta", "")
    self.query.bindValue(":finish", 0)
    self.query.exec()
    
    
    #sense_hat color example code
    a = int((p * 1271) % 256)
    b = int((p * 1271) % 256)
    c = int((p * 1271) % 256)
    self.sense.clear(a,b,c)
    
    #pass
  ##################################################

  #get sqldata -- motor part --
  def getQuery(self):
      query = QtSql.QSqlQuery("select * from command1 order by time desc limit 1");
      query.next()
      cmdTime = query.record().value(0)
      cmdType = query.record().value(1)
      cmdArg = query.record().value(2)
      is_finish = query.record().value(3)
      
      #print(is_finish)
      #print(cmdTime.toString(), cmdType, cmdArg)

      if is_finish == 0 :
        print(cmdTime.toString(), cmdType, cmdArg)
      
        ####for time sec########################
        if cmdArg.find("sec") :
          sec = ''
          numbers = re.findall("\d+",cmdArg)
          print("cmdArg : " + cmdArg)
          print(numbers)
          for i in numbers :
            sec += i
          print(sec)
       ########################################

        #print("zero")
    #detect new command
        #print(cmdTime.toString(), cmdType, cmdArg)
        
        #update
        query = QtSql.QSqlQuery("update command1 set is_finish=1 where is_finish=0");
    
        #motor move
        if cmdType == "go": self.go(int(sec))
        if cmdType == "back": self.back(int(sec))
        if cmdType == "left": self.left(int(sec))
        if cmdType == "right": self.right(int(sec))
        if cmdType == "mid": self.mid(int(sec))     
               
        #motor side move
        if cmdType == "front" and cmdArg == "press" : self.go("p")
        if cmdType == "leftside" and cmdArg == "press" : 
          self.go("p")
          self.left("p")
        if cmdType == "rightside" and cmdArg == "press" :
          self.go("p")
          self.right("p")
        
        # motor side stop
        if cmdType == "front" and cmdArg == "release" : self.stop()
        if cmdType == "leftside" and cmdArg == "release" : self.stop()
        if cmdType == "rightside" and cmdArg == "release" : self.stop()
               
  def go(self,sec):
    self.dcMotor.run(Raspi_MotorHAT.FORWARD)
    if sec != "p" :
      #self.sense.show_message("GO")
      #print("MOTOR GO")
      sleep(sec)
      # END
      self.dcMotor.run(Raspi_MotorHAT.RELEASE)

  def stop(self) :
    self.dcMotor.run(Raspi_MotorHAT.RELEASE)
    self.servo.setPWM(0,0,self.s_middle)

  def back(self,sec):
    self.dcMotor.run(Raspi_MotorHAT.BACKWARD)
    
    #self.sense.show_message("BACK")
    #print("MOTOR BACK")
    sleep(sec)
    # END
    self.dcMotor.run(Raspi_MotorHAT.RELEASE)
    
  def right(self,sec):
    self.servo.setPWM(0,0,self.s_right)
    if sec != "p" :
      #self.sense.show_message("RIGHT")
      #print("MOTOR RIGHT")
      sleep(sec)
      # END
      self.servo.setPWM(0,0,self.s_middle)
    
  def left(self,sec):
    self.servo.setPWM(0,0,self.s_left)
    if sec != "p" :
      sleep(sec)
      #self.sense.show_message("LEFT")
      # END
      self.servo.setPWM(0,0,self.s_middle)
    
  def mid(self,sec):
    self.servo.setPWM(0,0,self.s_middle)
    #sleep(sec)
    #self.sense.show_message("MID")
    #print("MOTOR MID")
  

th = pollingThread()
th.start()

app = QApplication([])

#infinity loop
while True: 
  pass