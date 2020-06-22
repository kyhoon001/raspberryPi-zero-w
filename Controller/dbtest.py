from PyQt5 import QtSql
from PyQt5.QtWidgets import *
from PyQt5.uic import *

# 타이머를 위한 import
from PyQt5.QtCore import *

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("db.ui",self)
        # db 연동부분임 
        self.db = QtSql.QSqlDatabase.addDatabase("QMYSQL")
        self.db.setHostName("3.34.124.67")
        self.db.setDatabaseName("16_9")
        self.db.setUserName("16_9")
        self.db.setPassword("1234")
        ok = self.db.open()
        print(ok)
        
        
        
        # 쿼리부분임 
        self.query = QtSql.QSqlQuery("select * from command1");
        
        while(self.query.next()):
            self.record = self.query.record()
            str = "%s | %6s | %5s | %d" % (self.record.value(0).toString(), self.record.value(1), self.record.value(2), self.record.value(3))
            self.text.appendPlainText(str)


        # 실시간 확인을 위해 함수와 연결해주는 1부분
        self.timer = QTimer()
        self.timer.setInterval(10) # 10ms
        self.timer.timeout.connect(self.pollingQuery)
        self.timer.start()


        
    def pollingQuery(self):
        
        #command log part
        self.query = QtSql.QSqlQuery("select * from command1 order by time desc limit 15");
        str = ""
        #self.text.clear()
        while(self.query.next()):
            self.record = self.query.record()
            str += "%s | %10s | %10s| %4d" % (self.record.value(0).toString(), self.record.value(1), self.record.value(2), self.record.value(3))
            self.text.setPlainText(str)
    
        
        #sensing log part
        self.query = QtSql.QSqlQuery("select * from sensing1 order by time desc limit 15");
        str = ""
        while(self.query.next()):
            self.record = self.query.record()
            str += "%s | %10s | %10s | %10s\n" % (self.record.value(0).toString(), self.record.value(1), self.record.value(2), self.record.value(3))
            self.text2.setPlainText(str)
    
    def commandQuery(self, cmd, arg):
        self.query.prepare("insert into command1 (time, cmd_string, arg_string, is_finish) values(:time, :cmd, :arg, :finish)");
        time = QDateTime().currentDateTime()
        self.query.bindValue(":time",time)
        self.query.bindValue(":cmd",cmd)
        self.query.bindValue(":arg",arg)
        self.query.bindValue(":finish",0)
        self.query.exec()
    


    def clickedRight(self) :
        
        '''
        #insert 예시코드 해당 코드는 따로 함수로 만들어서 위로 뺐음.
        
        self.query.prepare("insert into command1(time, cmd_string, arg_string, is_finish) values(:time,:cnd,:arg,:finish)");
        time = QDateTime().currentDateTime()
        self.query.bindValue(":time",time)
        self.query.bindValue(":cmd","right")
        self.query.bindValue(":arg","1 sec")
        self.query.bindValue(":finish",0)
        self.query.exec()
        '''
        #print(self.timer_s.text())
        
        
        #if self.timer_s.text() == "":
            #self.commandQuery("right","1 sec")
        #else :
            #self.commandQuery("right",self.timer_s.text() + " sec")
            
        self.commandQuery("right","1 sec")

    def clickedLeft(self) :
        self.commandQuery("left","1 sec")
        
    def clickedGo(self) :
        if self.timer_s.text() == "":
            self.commandQuery("go","1 sec")
        else :
            self.commandQuery("go",self.timer_s.text() + " sec")
        
    def clickedBack(self) :
        self.commandQuery("back","1 sec")
        
    def clickedMid(self) :
        self.commandQuery("mid","1 sec")
        
    def leftPress(self) :
        self.commandQuery("leftside","press")
    def leftRelease(self) :
        self.commandQuery("leftside","release")
        
    def rightPress(self) :
        self.commandQuery("rightside","press")
    def rightRelease(self) :
        self.commandQuery("rightside","release")
        
    def frontPress(self) :
        self.commandQuery("front","press")
    def frontRelease(self) :
        self.commandQuery("front","release")
        
app = QApplication([])
win = MyApp()
win.show()
app.exec()