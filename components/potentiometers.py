import time

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import board
import busio

def map_range(value, from_min, from_max, to_min, to_max):
    normalized = (value - from_min) / (from_max - from_min)
    mapped_value = to_min + (normalized * (to_max - to_min))
    return mapped_value

def map_value(x, in_min=0.0, in_max=3.305, out_min=0.0, out_max=100.0):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

class Potentiometers:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS.ADS1115(i2c, address=0x48)
        self.__ch0 = AnalogIn(ads, ADS.P0)
        self.__ch1 = AnalogIn(ads, ADS.P1)
        self.__ch2 = AnalogIn(ads, ADS.P2)

    def get_value(self, channel):
        match (channel):
            case 0:
                return self.__ch0.voltage
            case 1:
                return self.__ch1.voltage
            case 2:
                return self.__ch2.voltage
        return None

    def get_percent(self, channel):
        raw_value = self.get_value(channel)
        return map_value(raw_value)