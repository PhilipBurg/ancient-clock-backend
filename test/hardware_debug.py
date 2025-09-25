import threading
from signal import pause

from gpiozero import Button

from components.buttons import BUTTONS, TOGGLE_SWITCHES
from components.displays import DISPLAYS, Display
from components.potentiometers import Potentiometers

def define_action_for_press(button: Button, display: Display):
    button.when_activated = lambda: display.show_text('ON')
    button.when_deactivated = lambda: display.show_text('OFF')

for i in range(4):
    DISPLAYS[i].show_text('ON' if TOGGLE_SWITCHES[i].value else 'OFF')
    define_action_for_press(TOGGLE_SWITCHES[i], DISPLAYS[i])

for i in range(4):
    DISPLAYS[i + 4].show_text('ON' if BUTTONS[i].value else 'OFF')
    define_action_for_press(BUTTONS[i], DISPLAYS[i + 4])

def potentiometer_work_thread():
    pots = Potentiometers()
    while True:
        DISPLAYS[8].show_text(f"{pots.get_percent(0):.1f}")
        DISPLAYS[9].show_text(f"{pots.get_percent(1):.1f}")
        DISPLAYS[10].show_text(f"{pots.get_percent(2):.1f}")


potentiometer_work_thread = threading.Thread(target=potentiometer_work_thread)
potentiometer_work_thread.start()

pause()