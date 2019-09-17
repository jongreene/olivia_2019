# -*- coding:UTF-8 -*-
import os
#--------------Driver Library-----------------#
import RPi.GPIO as GPIO
import OLED_Driver as OLED
#--------------Image Library---------------#
from PIL  import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor
from time import sleep
import datetime

GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print "---- LCD ----"

return_state = "slide"
current_state = "slide"

def changeState(next_state):
    global return_state
    global current_state
    if(current_state is "off" and next_state is "off"):
        current_state = return_state
    elif(next_state is "off"):
        screenOff()
        return_state = current_state
        current_state = "off"
    elif(next_state is not current_state):
        current_state = next_state

def Display_Picture(File_Name):
    image = Image.open(File_Name)
    OLED.Display_Image(image)

def rightPress(channel):
	changeState("clock")

def leftPress(channel):
	changeState("slide")

def middlePress(channel):
	changeState("off")

GPIO.add_event_detect(4, GPIO.FALLING, callback=rightPress, bouncetime=300)
GPIO.add_event_detect(3, GPIO.FALLING, callback=middlePress, bouncetime=300)
GPIO.add_event_detect(2, GPIO.FALLING, callback=leftPress, bouncetime=300)

def screenOff():
    GPIO.setmode(GPIO.BCM)
    OLED.Clear_Screen()

def clock():
	currentDT = datetime.datetime.now()
	print (str(currentDT))
	image = Image.new("RGB", (OLED.SSD1351_WIDTH, OLED.SSD1351_HEIGHT), "BLACK")
	draw = ImageDraw.Draw(image)
	font = ImageFont.truetype('cambriab.ttf',22)
	font = ImageFont.truetype('cambriab.ttf',30)
	draw.text((0, 0), 'I love', fill = "WHITE", font = font)
	draw.text((0, 34), 'you!', fill = "WHITE",font = font)
	draw.text((0, 70), currentDT.strftime("%H:%M:%S"), fill = "WHITE",font = font)
	OLED.Display_Image(image)
	OLED.Delay(1)

def slideShow():
	global current_state
	for root, dirs, files in os.walk("images", topdown=False):
		if(current_state is not "slide"):
			break
		for name in files:
			if(current_state is not "slide"):
				break
			Display_Picture(os.path.join(root, name))
			OLED.Delay(5000)

def loop():
	if(current_state is "slide"):
		slideShow()
	elif(current_state is "clock"):
		clock()
	else:
		OLED.Clear_Screen()

try:
	OLED.Device_Init()
	while (1):
		loop()
		sleep(0.01)

except KeyboardInterrupt:
	GPIO.setmode(GPIO.BCM)
	OLED.Clear_Screen()
	GPIO.cleanup()       # clean up GPIO on CTRL+C exit

GPIO.cleanup()           # clean up GPIO on normal exit

print "---- LCD ----"
