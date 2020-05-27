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

## 여기부터 시간 관련
TimeZone = timezone(timedelta(hours= +9))
font = ImageFont.load_default()
dateString = '%A %d %B %Y'
timeString = '%-l:%M:%S'
timeString2 = ' %p'

def printmode():
    global MODE_BUTTON
    if MODE_BUTTON == 0 :
        strDate = datetime.now(TimeZone).strftime(dateString)
        result = datetime.now(TimeZone).strftime(timeString)
        tresult = datetime.now(TimeZone).strftime(timeString2)

        draw.rectangle((0,0,width,height),outline=0,fill=0)
        draw.text((x,top),strDate,font=font_small,fill=255)
        draw.text((x+8,top+14),result, font=font_big, fill=255)
        draw.text((x+70,top+20),tresult, font=font_middle, fill=255)
        draw.line((0, top+12, 127, top+12),fill=100)


            #disp.image(image)
            #disp.display()
            #time.sleep(.1)
    #elif MODE_BUTTON == 1:
    else :
        strDate = datetime.now(TimeZone).strftime(dateString)
        result = datetime.now(TimeZone).strftime(timeString)
        tresult = datetime.now(TimeZone).strftime(timeString2)

        draw.rectangle((0,0,width,height),outline=0,fill=0)
        draw.text((x,top),strDate,font=font_small,fill=255)

            #disp.image(image)
            #disp.display()
            #time.sleep(.1)


try:
    while True:
        printmode()
        disp.image(image)
        disp.display()
        time.sleep(.1)

    """
    if MODE_BUTTON == 0 :
        while True:
            strDate = datetime.now(TimeZone).strftime(dateString)
            result = datetime.now(TimeZone).strftime(timeString)
            tresult = datetime.now(TimeZone).strftime(timeString2)

            draw.rectangle((0,0,width,height),outline=0,fill=0)
            draw.text((x,top),strDate,font=font_small,fill=255)
            draw.text((x+8,top+14),result, font=font_big, fill=255)
            draw.text((x+70,top+20),tresult, font=font_middle, fill=255)
            draw.line((0, top+12, 127, top+12),fill=100)


            disp.image(image)
            disp.display()
            time.sleep(.1)
    else :
            strDate = datetime.now(TimeZone).strftime(dateString)
            result = datetime.now(TimeZone).strftime(timeString)
            tresult = datetime.now(TimeZone).strftime(timeString2)

            draw.rectangle((0,0,width,height),outline=0,fill=0)
            draw.text((x,top),strDate,font=font_small,fill=255)

            disp.image(image)
            disp.display()
            time.sleep(.1)
"""
except KeyboardInterrupt:
    print("Cleaning up!")
    GPIO.cleanup()
