import time
import pygame
import threading
from riddles.pot_riddle import PotRiddle
from riddles.lightsout import LightsOut
from riddles.word_riddle import WordRiddle
from components.buttons import TOGGLE_SWITCHES, BUTTONS
from components.displays import DISPLAYS
from components.neopixels import NEOPIXELS
from components.speaker import SUCCESS_SOUND, say, generate_speech
from gpiozero import Device
from components.clock import start_clock, stop_clock

def shutdown_alarm():
    say(generate_speech("super, ich schalte mich nun aus"))
    time.sleep(1)

    # stop all sounds
    pygame.mixer.stop()  
    pygame.mixer.quit() 

    NEOPIXELS.stop()

    # Displays off
    for d in DISPLAYS:
        try:
            d.clear()
        except AttributeError:
            pass  # if DummyDisplay
    
    stop_clock() 

    # close GPIO-Threads clean
    Device.pin_factory.close()

class RiddleManager:
    def __init__(self):
        self.current = None

    def start(self, pot_riddle: dict, lightsout: dict, word_riddle: dict):
        threading.Thread(target=start_clock, daemon=True).start()
        say(generate_speech("Guten Morgen!"))
        self.start_pot(pot_riddle, lightsout, word_riddle)

    def start_pot(self, pot_target, lightsout, word_riddle):
        self.current = PotRiddle(
            introduction=f"Drehe die drei Knöpfe so, dass ihre Summe {pot_target} ergibt!",
            on_fail=["Noch nicht richtig!", "Probier es weiter."],
            on_solve="du hast es geschafft!",
            target_sum=pot_target,
            on_solved_callback=lambda: self.start_lights(lightsout, word_riddle)
        )
        self.current.start()

    def start_lights(self, lightsout, word_riddle):
        self.current = LightsOut(
            correct_glyph="Scarab",
            incorrect_glyph=[s for s in lightsout if s != "Scarab"],
            #incorrect_glyph=["Fish", "Goose", "Turtle", "Falcon"],
            toggles=TOGGLE_SWITCHES,
            displays=DISPLAYS[:4],
            introduction="Schnappe den Käfer",
            on_fail=["Leider falsch", "Versuche es weiter!"],
            on_solve="du hast das Rätsel gelöst!",
            on_solved_callback=lambda: self.start_word(word_riddle)
        )
        self.current.start()

    def start_word(self, word_data):
        self.current = WordRiddle(
            #word="HAUS",
            word=word_data["word"],
            letters=word_data["letters"], 
            buttons=BUTTONS,
            displays=DISPLAYS[4:8],
            introduction="Ordne die Buchstaben zu einem sinnvollen Wort!",
            on_fail=["Versuch es nochmal!", "leider falsch"],
            on_solve=f"Sehr gut, das Wort lautet {word_data['word']}!",
            on_solved_callback=shutdown_alarm 
        )
        self.current.start()
