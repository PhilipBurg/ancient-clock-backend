import random
from gpiozero import Button
from components.displays import Display
from components.neopixels import NEOPIXELS
from components.speaker import SUCCESS_SOUND, say, generate_speech

CHECKMARK_PATH = "./assets/checkmark.png"
PROPABILITY_COMMENT_ON_FAIL = 0.35


class WordRiddle:
    def __init__(
        self,
        word: str,               # Zielwort, z.B. "HAUS"
        buttons: list[Button],   # GPIO-Buttons
        displays: list[Display], # Displays für die Buchstaben
        introduction: str,
        on_fail: list[str],
        on_solve: str
    ):
        self.word = list(word.upper())     # ["H","A","U","S"]

        # Buchstaben zufällig verteilen
        self.letters = self.word.copy()
        random.shuffle(self.letters)       # z.B. ["U","S","A","H"]

        self.buttons = buttons
        self.displays = displays
        self.progress = []

        self.introduction = generate_speech(introduction)
        self.on_fail = [generate_speech(n) for n in on_fail]
        self.on_solve = generate_speech(on_solve)

        # Displays zeigen die zufälligen Buchstaben
        for i, d in enumerate(self.displays):
            if i < len(self.letters):
                d.show_text(self.letters[i])

        # Buttons mit den geshuffelten Buchstaben verbinden
        for btn, letter in zip(self.buttons, self.letters):
            btn.when_pressed = lambda l=letter: self.press(l)

    def press(self, letter):
        self.progress.append(letter)
        print("Eingabe:", self.progress)

        if self.progress == self.word:
            self.handle_solved()
        elif not self.word[:len(self.progress)] == self.progress:
            self.handle_failed()

    def start(self):
        say(self.introduction)
        NEOPIXELS.start_continuous(0.7)

    def stop(self):
        for btn in self.buttons:
            btn.when_pressed = None
        for d in self.displays:
            d.show_asset(CHECKMARK_PATH)

    def handle_failed(self):
        self.progress = []
        say(random.choice(self.on_fail))
        # Displays zurück auf die Start-Anordnung
        for i, d in enumerate(self.displays):
            if i < len(self.letters):
                d.show_text(self.letters[i])

    def handle_solved(self):
        if self.progress != self.word:
            return
        self.stop()
        SUCCESS_SOUND.play()
        say(self.on_solve)
        NEOPIXELS.start_sine_blink_and_sleep((100, 255, 0), 6, 0.2)
        NEOPIXELS.start_continuous(0.3)
