import pygame
import time
import random
from gpiozero import Button
from signal import pause

from components.speaker import generate_speech, say
from components.neopixels import NEOPIXELS
pygame.mixer.init()


ALARM_SOUND = pygame.mixer.Sound("./assets/ancient_egypt.wav")


def start_alarm():
    print(" Wecker startet...")
    # Hintergrundsound starten
    ALARM_SOUND.set_volume(0.8)
    ALARM_SOUND.play(-1)  # Endlosschleife

    
    filename = generate_speech("Willkommen, löse meine Rätsel im Nu und ich lass dich in Ruh", local=True)
    say(filename)
    time.sleep(5)  # warten, bis gesprochen wurde


def stop_alarm():
    print(" Button gedrückt – Wecker aus, LEDs werden grün.")
    ALARM_SOUND.stop()
    NEOPIXELS.start_sine_blink_and_sleep((0, 255, 0), 3, 0.3)  # grüne Animation
    NEOPIXELS.start_continuous(0.3)


# Button auf GPIO 17 
button = Button(17)
button.when_pressed = stop_alarm


start_alarm()
pause()
