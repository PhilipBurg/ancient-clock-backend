from riddles.pot_riddle import PotRiddle
from riddles.lightsout import LightsOut
from riddles.word_riddle import WordRiddle
from components.buttons import TOGGLE_SWITCHES, BUTTONS
from components.displays import DISPLAYS

class RiddleManager:
    def __init__(self):
        self.current = None

    def start(self):
        self.start_pot()

    def start_pot(self):
        self.current = PotRiddle(
            introduction="Drehe die drei Knöpfe so, dass ihre Summe genau 100 ergibt!",
            on_fail=["Noch nicht richtig!", "Probier es weiter."],
            on_solve="Sehr gut, du hast es geschafft!",
            on_solved_callback=self.start_lights
        )
        self.current.start()

    def start_lights(self):
        self.current = LightsOut(
            correct_glyph="Scarab",
            incorrect_glyph=["Fish", "Goose", "Turtle", "Falcon"],
            toggles=TOGGLE_SWITCHES,
            displays=DISPLAYS[:4],
            introduction="Wähle nur den Käfer aus.",
            on_fail=["Das ist leider noch nicht des Rätsels Lösung", "Versuche es weiter!"],
            on_solve="Herzlichen Glückwunsch, du hast das Rätsel gelöst!",
            on_solved_callback=self.start_word
        )
        self.current.start()

    def start_word(self):
        self.current = WordRiddle(
            word="HAUS",
            buttons=BUTTONS,
            displays=DISPLAYS[4:8],
            introduction="Ordne die Buchstaben zu einem sinnvollen Wort!",
            on_fail=["Das war falsch, versuch es nochmal!"],
            on_solve="Sehr gut, das Wort lautet HAUS!"
        )
        self.current.start()
