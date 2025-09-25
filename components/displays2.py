import adafruit_ssd1306
import adafruit_tca9548a
import board
import busio
from board import I2C

from components.imagegenerator import ImageGenerator

DISPLAY_I2C_ADDRESS = 0x3C
OLED_WIDTH, OLED_HEIGHT = 128, 64


class displays2:

    def __init__(self, i2c: I2C):
        self.__oled = adafruit_ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c, addr=DISPLAY_I2C_ADDRESS)
        self.__text_image_generator = ImageGenerator()

    def show_text(self, text):
        img = self.__text_image_generator.generate_text_image(text)
        self.__oled.image(img)
        self.__oled.show()


i2c = busio.I2C(board.SCL, board.SDA)

MULTIPLEXERS = [
    adafruit_tca9548a.TCA9548A(i2c, address=0x70),
    adafruit_tca9548a.TCA9548A(i2c, address=0x71)
]

DISPLAYS = [
    displays2(MULTIPLEXERS[0][3]),
    displays2(MULTIPLEXERS[0][4]),
    displays2(MULTIPLEXERS[0][5]),
    displays2(MULTIPLEXERS[0][6]),
    displays2(MULTIPLEXERS[0][2]),
    displays2(MULTIPLEXERS[0][1]),
    displays2(MULTIPLEXERS[0][0]),
    displays2(MULTIPLEXERS[0][7]),
    displays2(MULTIPLEXERS[1][5]),
    displays2(MULTIPLEXERS[1][6]),
    displays2(MULTIPLEXERS[1][3])
]

for d in DISPLAYS:
    d.show_text("Hallo")
