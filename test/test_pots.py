import time
import sys
import os

# Damit "components" gefunden wird (eine Ebene höher als test/)
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from components.potentiometers import Potentiometers

pots = Potentiometers()

try:
    while True:
        v0 = pots.get_value(0)
        v1 = pots.get_value(1)
        v2 = pots.get_value(2)
        print(f"Ch0: {v0:.3f} V  |  Ch1: {v1:.3f} V  |  Ch2: {v2:.3f} V")
        time.sleep(0.5)
except KeyboardInterrupt:
    print("Abbruch")
