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


font_small = ImageFont.truetype("malgun.ttf",8)    # 폰트 준비
font_big = ImageFont.truetype("malgun.ttf", 17)
font_middle = ImageFont.truetype("malgun.ttf", 11)

disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST,dc=DC,spi=SPI.SpiDev(SPI_PORT,SPI_DEVICE,max_speed_hz=8000000))

disp.begin()
disp.clear()
disp.display()

width = disp.width
height = disp.height
image = Image.new('1',(width,height))
draw = ImageDraw.Draw(image)
TimeZone = timezone(timedelta(hours= +9))


draw.rectangle((0,0,width,height),outline=0,fill=0)

padding = -2
top = padding
bottom =  height - padding
x = 0

font = ImageFont.load_default()
dateString = '%A %d %B %Y'
timeString = '%-l:%M:%S'
timeString2 = ' %p'

try:
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

except KeyboardInterrupt:
    print("Cleaning up!")
    GPIO.cleanup()
