from os import PathLike
from time import sleep

import adafruit_ssd1306
import adafruit_tca9548a
import board
import busio
from PIL import Image
from board import I2C

from components.imagegenerator import ImageGenerator, CLEAR, HIEROGLYPHS

DISPLAY_I2C_ADDRESS = 0x3C
OLED_WIDTH, OLED_HEIGHT = 128, 64

MAX_CONNECTION_TRIES = 5


class Display:

    def __init__(self, i2c: I2C):
        self.__i2c = i2c
        self.__text_image_generator = ImageGenerator()
        self.__oled = None
        self._init_display()

    def _init_display(self):
        for attempt in range(MAX_CONNECTION_TRIES):
            try:
                self.__oled = adafruit_ssd1306.SSD1306_I2C(
                    OLED_WIDTH, OLED_HEIGHT, self.__i2c,
                    addr=DISPLAY_I2C_ADDRESS
                )
                return
            except Exception as e:
                if attempt + 1 == MAX_CONNECTION_TRIES:
                    raise e
                else:
                    sleep(0.02 + 0.01 * attempt)

    def show_text(self, text):
        img = self.__text_image_generator.generate_text_image(text)
        self.__oled.image(img)
        self.__oled.show()

    def clear(self):
        self.__oled.image(CLEAR)
        self.__oled.show()

    def show_hieroglyph(self, glyph):
        img = self.__text_image_generator.generate_hieroglyph(glyph)
        self.__oled.image(img)
        self.__oled.show()

    def show_asset(self, asset):
        img = Image.open(asset).convert("1")
        self.__oled.image(img)
        self.__oled.show()


class DummyDisplay:

    def __init__(self, number):
        self.__number = number

    def show_text(self, text):
        print(f"Dummy display {self.__number} show text {text}")

    def clear(self):
        print(f"Dummy display {self.__number} clear")

    def show_hieroglyph(self, glyph):
        print(f"Dummy display {self.__number} show hieroglyph {HIEROGLYPHS[glyph]}")

    def show_asset(self, asset):
        print(f"Dummy display {self.__number} show asset {asset}")


i2c = busio.I2C(board.SCL, board.SDA)

MULTIPLEXERS = [
    adafruit_tca9548a.TCA9548A(i2c, address=0x70),
    adafruit_tca9548a.TCA9548A(i2c, address=0x71)
]

DISPLAYS = [
    Display(MULTIPLEXERS[0][3]),
    Display(MULTIPLEXERS[0][4]),
    Display(MULTIPLEXERS[0][5]),
    Display(MULTIPLEXERS[0][6]),
    Display(MULTIPLEXERS[0][0]),
    Display(MULTIPLEXERS[0][7]),
    # Weird hardware issue. These displays are sometimes defective
    Display(MULTIPLEXERS[0][2]), # DummyDisplay(4),
    Display(MULTIPLEXERS[0][1]), # DummyDisplay(5),
    Display(MULTIPLEXERS[1][5]),
    Display(MULTIPLEXERS[1][6]),
    Display(MULTIPLEXERS[1][3])
]
