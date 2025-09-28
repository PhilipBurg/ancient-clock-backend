import time, board, busio
from adafruit_ht16k33 import segments

i2c = busio.I2C(board.SCL, board.SDA)
display = segments.Seg7x4(i2c, address=0x72)
display.brightness = 0.5
display.colon = True
_running = True

def start_clock():
    global _running
    _running = True
    while _running:
        now = time.localtime()
        display.print(f"{now.tm_hour:02d}{now.tm_min:02d}")
        time.sleep(1)

def stop_clock():
    global _running
    _running = False
    display.fill(0)
