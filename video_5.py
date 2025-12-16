import os
import time
import logging
import spidev as SPI
from lib import LCD_1inch83
from PIL import Image

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0 
device = 0 
logging.basicConfig(level = logging.DEBUG)

try:
    ''' Warning!!!Don't  creation of multiple displayer objects!!! '''
    #disp = LCD_1inch83.LCD_1inch83(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
    disp = LCD_1inch83.LCD_1inch83()
    # Initialize library.
    disp.Init()
    # Clear display.
    disp.clear()
    #Set the backlight to 100
    disp.bl_DutyCycle(50)
    frame = 1
    while True:
        print("showing a frame")
        if not os.path.exists(f"frames/frame_{frame:04}.png"):
            frame = 1
        frame_img = Image.open(f"frames/frame_{frame:04}.png")
        disp.ShowImage(frame_img)
        frame += 1
        time.sleep(1/60)
    
except IOError as e:
    logging.info(e)    
    
except KeyboardInterrupt:
    disp.module_exit()
    logging.info("quit:")
    exit()
