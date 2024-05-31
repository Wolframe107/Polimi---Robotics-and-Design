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

    # Create blank image for drawing.
    image = Image.new("RGB", (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(image)
    font18 = ImageFont.truetype("../Font/Font00.ttf",18) 
    
    #im_r=image.rotate(90)
    disp.ShowImage(image)

    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)         # 1/timeout is the frequency at which the port is read
    
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            logging.info("reading")
            if line == "0":
                logging.info(line)
                image = Image.open('../pic/picture1.jpg')	
                im_r=image.rotate(0)
                disp.ShowImage(im_r)

            if line == "1":
                logging.info(line)
                image = Image.open('../pic/picture2.jpg')	
                im_r=image.rotate(0)
                disp.ShowImage(im_r)
    
    disp.module_exit()
    logging.info("quit:")
    
except IOError as e:
    logging.info(e)    
except KeyboardInterrupt:
    disp.module_exit()
    logging.info("quit:")
    exit()
