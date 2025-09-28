import time
import board
import busio
from adafruit_ht16k33 import segments

# initialize I²C bus 
i2c = busio.I2C(board.SCL, board.SDA)


display = segments.Seg7x4(i2c, address=0x72)

# the brightness (0.0–1.0)
display.brightness = 0.5


display.colon = True

# show for just 10 sec 
for _ in range(10):
    now = time.localtime()
    display.print(f"{now.tm_hour:02d}{now.tm_min:02d}")
    time.sleep(1)

# delete display
display.fill(0)
