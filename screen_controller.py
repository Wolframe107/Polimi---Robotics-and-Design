#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import chardet
import os
import sys 
import time
import logging
import spidev as SPI
import serial
sys.path.append("..")
from lib import LCD_1inch8
from PIL import Image,ImageDraw,ImageFont

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0 
device = 0 
logging.basicConfig(level=logging.DEBUG)

try:
	# display with hardware SPI:
	''' Warning!!!Don't  creation of multiple displayer objects!!! '''
	#disp = LCD_1inch8.LCD_1inch8(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
	disp = LCD_1inch8.LCD_1inch8()
	Lcd_ScanDir = LCD_1inch8.SCAN_DIR_DFT  #SCAN_DIR_DFT = D2U_L2R
	# Initialize library.
	disp.Init()
	# Clear display.
	disp.clear()
	#Set the backlight to 100
	disp.bl_DutyCycle(50)
 
except IOError as e:
	logging.info(e)    
except KeyboardInterrupt:
	disp.module_exit()
	logging.info("quit:")
	exit()

def screen_controller_start():
	logging.info("Started the face :)")
	image = Image.open('pic/booting.jpg')	
	im_r=image.rotate(0)
	disp.ShowImage(im_r)

def screen_shutdown():
	logging.info("Shutting down screen")
	disp.module_exit()
	

def set_face(mode):
	
	if mode == "homing" :
		#logging.info("Switching to Homing")
		
		image = Image.open('pic/homing.jpg')	
		im_r=image.rotate(0)
		disp.ShowImage(im_r)
	
	if mode == "working" :
		#logging.info("Switching to Working")
		
		image = Image.open('pic/working.jpg')	
		im_r=image.rotate(0)
		disp.ShowImage(im_r)
		
	if mode == "angry" :
		#logging.info("Switching to angry face")
		
		image = Image.open('pic/angry.jpg')	
		im_r=image.rotate(0)
		disp.ShowImage(im_r)
	
