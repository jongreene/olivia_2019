# -*- coding:UTF-8 -*-

#--------------Driver Library-----------------#
import RPi.GPIO as GPIO
import OLED_Driver as OLED
#--------------Image Library---------------#
from PIL  import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor
from time import sleep

GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print "---- LCD ----"

display_on = True

def middlePress():
    global display_on
    display_on = not display_on
    GPIO.setmode(GPIO.BCM)
    OLED.Clear_Screen()

def Display_Picture(File_Name):
    image = Image.open(File_Name)
    OLED.Display_Image(image)

def my_callback(channel):
    print "right press"
    Display_Picture("picture1.jpg")

def my_callback2(channel):
    print "left press"
    Display_Picture("picture2.jpg")

def my_callback3(channel):
    print "middle press"
    middlePress()

GPIO.add_event_detect(4, GPIO.FALLING, callback=my_callback, bouncetime=300)
GPIO.add_event_detect(3, GPIO.FALLING, callback=my_callback3, bouncetime=300)
GPIO.add_event_detect(2, GPIO.FALLING, callback=my_callback2, bouncetime=300)

try:
	OLED.Device_Init()
	while (1):
		if(display_on):
			Display_Picture("picture1.jpg")
			OLED.Delay(5000)
		if(display_on):
			Display_Picture("picture2.jpg")
			OLED.Delay(5000)
		if(display_on):
			Display_Picture("picture3.jpg")
			OLED.Delay(5000)
		if(display_on):
			Display_Picture("picture4.jpg")
			OLED.Delay(5000)
		if(display_on):
			Display_Picture("picture5.jpg")
			OLED.Delay(5000)
		sleep(0.01)

except KeyboardInterrupt:
	GPIO.setmode(GPIO.BCM)
	OLED.Clear_Screen()
	GPIO.cleanup()       # clean up GPIO on CTRL+C exit

GPIO.cleanup()           # clean up GPIO on normal exit

print "---- LCD ----"

