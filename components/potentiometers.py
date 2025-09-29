"""import time

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
        return map_value(raw_value)  """
"""
import board
import busio
import adafruit_tca9548a
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

def map_value(x, in_min=0.0, in_max=3.305, out_min=0.0, out_max=100.0):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

class Potentiometers:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)

        # Direkter Zugriff: MUX 0x70, Kanal 0, ADS1115 @ 0x4A
        mux = adafruit_tca9548a.TCA9548A(i2c, address=0x70)
        try:
            ads = ADS.ADS1115(mux[0], address=0x4A)
            # Testprobe
            AnalogIn(ads, ADS.P0).voltage
            print("ADS1115 gefunden: 0x4A @ MUX 0x70, Kanal 0")
        except Exception:
            raise RuntimeError("ADS1115 nicht erreichbar auf 0x4A @ MUX 0x70 Kanal 0!")

        self.ads = ads
        # Kanäle vorbereiten
        self.__ch0 = AnalogIn(self.ads, ADS.P0)
        self.__ch1 = AnalogIn(self.ads, ADS.P1)
        self.__ch2 = AnalogIn(self.ads, ADS.P2)

    def get_value(self, channel):
        if channel == 0:
            return self.__ch0.voltage
        elif channel == 1:
            return self.__ch1.voltage
        elif channel == 2:
            return self.__ch2.voltage
        return None

    def get_percent(self, channel):
        raw_value = self.get_value(channel)
        return map_value(raw_value) if raw_value is not None else None

"""
import board
import busio
import adafruit_tca9548a
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

def map_value(x, in_min=0.0, in_max=3.305, out_min=0.0, out_max=100.0):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


class Potentiometers:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)

        mux = adafruit_tca9548a.TCA9548A(i2c, address=0x70)
        self.ads = None

        # alle 4 Standard-Adressen durchprobieren
        for addr in [0x48, 0x49, 0x4A, 0x4B]:
            try:
                ads = ADS.ADS1115(mux[0], address=addr)
                # Test-Leseprobe
                AnalogIn(ads, ADS.P0).voltage
                print(f"ADS1115 gefunden: 0x{addr:02X} @ MUX 0x70 Kanal 0")
                self.ads = ads
                break
            except Exception:
                continue

        if not self.ads:
            raise RuntimeError("Kein ADS1115 auf 0x48–0x4B gefunden!")

        # Kanäle vorbereiten
        self.__ch0 = AnalogIn(self.ads, ADS.P0)
        self.__ch1 = AnalogIn(self.ads, ADS.P1)
        self.__ch2 = AnalogIn(self.ads, ADS.P2)

    def get_value(self, channel):
        if channel == 0:
            return self.__ch0.voltage
        elif channel == 1:
            return self.__ch1.voltage
        elif channel == 2:
            return self.__ch2.voltage
        return None

    def get_percent(self, channel):
        raw_value = self.get_value(channel)
        return map_value(raw_value) if raw_value is not None else None
