import time
from datetime import timezone, timedelta, datetime
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import RPi.GPIO as GPIO

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

RST = None
DC = 25
SPI_PORT = 0
SPI_DEVICE = 0
MODE_BUTTON = 5
mode = 0 # mode가 0이면 시계를 키고, 1이면 달력을 키게끔 하고싶음.

global image
# 버튼에 대한 부분
GPIO.setmode(GPIO.BCM)
button = MODE_BUTTON
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

## 버튼 눌렀을 때 함수.
def buttonPressed(channel) :
    global mode
    print(f"button @{channel} pressed!")

    if channel == MODE_BUTTON :
        print(f"mode : {mode}")
        if mode == 1 : mode = 0
        else : mode = 1

# 버튼을 활용한 인터럽트 스레드
GPIO.add_event_detect(button, GPIO.FALLING, callback=buttonPressed, bouncetime=200)

# 폰트
font_small = ImageFont.truetype("malgun.ttf",8)    # 폰트 준비
font_big = ImageFont.truetype("malgun.ttf", 17)
font_middle = ImageFont.truetype("malgun.ttf", 11)

#disp 관련
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST,dc=DC,spi=SPI.SpiDev(SPI_PORT,SPI_DEVICE,max_speed_hz=8000000))

disp.begin()
disp.clear()
disp.display()

width = disp.width
height = disp.height
image = Image.new('1',(width,height))
draw = ImageDraw.Draw(image)

draw.rectangle((0,0,width,height),outline=0,fill=0)

padding = -2
top = padding
bottom =  height - padding
x = 0


#가운데 정렬 관련
def getTextCenterAlignXY(text, font): #width : 128 ,, height : 64
        centerX = (128 -  draw.textsize(text,font=font)[0]) // 2
        centerY = (64 - draw.textsize(text, font=font)[1]) // 2
        return (centerX, centerY)

#우리나라 시간대로 맞추기 위한 타임존
TimeZone = timezone(timedelta(hours= +9))
def printmode():
    global mode
    global image
    if mode == 0 : #이게 시계모드
        
        #시계 포맷
        font = ImageFont.load_default()
        dateString = '%A %d %B %Y'
        timeString = '%-l:%M:%S'
        timeString2 = ' %p'

        # 화면 까맣게 초기화를 위한 코드 2줄
        image = Image.new('1',(width,height))
        draw = ImageDraw.Draw(image)

        strDate = datetime.now(TimeZone).strftime(dateString)
        result = datetime.now(TimeZone).strftime(timeString)
        tresult = datetime.now(TimeZone).strftime(timeString2)

        draw.rectangle((0,0,width,height),outline=0,fill=0)
        draw.text((x,top),strDate,font=font_small,fill=255)
        draw.text((x+8,top+14),result, font=font_big, fill=255)
        draw.text((x+70,top+20),tresult, font=font_middle, fill=255)
        draw.line((0, top+12, 127, top+12),fill=100)


    else : #이건 달력모드

        # 화면 까맣게 초기화를 위한 코드 2줄
        image = Image.new('1',(width,height))
        draw = ImageDraw.Draw(image)

        # 오늘 날짜 정보
        dd = datetime.now(TimeZone)
        year = str(dd.year) + "년"    # 년도
        month = str(dd.month) + "월"  # 월
        day = str(dd.day)+"일"  # 일


        draw.text(( x,top), "Calander", font = font_small, fill=1 ) 
        draw.text(( getTextCenterAlignXY(year, font_middle)[0],2), year, font = font_middle, fill=1 ) 
        #15가 중간정도임 y축
        draw.text((5,15), month, font = font_middle, fill=1 ) 
        draw.text((0+len(month)*13+5,15), day, font = font_middle, fill=1 ) 
        days = '월화수목금토일'[dd.weekday()] # weekday(): 요일을 0~6으로 리턴
        draw.text((62,10), days+'요일', font = font_big, fill=1)



try:
    disp.clear()
    disp.display()
    while True:
        printmode()
        disp.image(image)
        disp.display()
        time.sleep(.1)

except KeyboardInterrupt:
    print("Cleaning up!")
    GPIO.cleanup()
