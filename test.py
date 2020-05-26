from PIL import Image, ImageDraw, ImageFont 
 
im = Image.new('1', (128,64),0)
draw = ImageDraw.Draw(im) 
 
font = ImageFont.truetype("malgun.ttf",15) 
 
draw.text( (10,10), '''세종대왕  만만세''', font=font,fill=1) 
 
im.show() 