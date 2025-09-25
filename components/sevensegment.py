import threading
from datetime import datetime
from time import sleep

import board
import busio

from adafruit_ht16k33 import segments

class SevenSegment:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.__display = segments.Seg7x4(i2c, address=0x72)
        self.__display.brightness = 1
        self.__display.auto_write = False
        self.__running = False
        self.__thread = None

    def __update_clock(self):
        now = datetime.now()
        self.__display.fill(False)
        self.__display.print(now.strftime("%H%M"))
        self.__display.colon = datetime.now().second % 2 == 1
        self.__display.show()

    def __clock_thread(self):
        while self.__running:
            self.__update_clock()
            sleep(0.01)

    def start(self):
        self.__thread = threading.Thread(target=self.__clock_thread)
        self.__running = True
        self.__thread.start()

    def stop(self):
        self.__running = False
        if self.__thread is not None:
            self.__thread.join()
        self.__display.fill(False)
        self.__display.show()