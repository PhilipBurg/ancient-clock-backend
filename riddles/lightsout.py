import random
from signal import pause
from gpiozero import Button

from components.buttons import TOGGLE_SWITCHES
from components.displays import Display, DISPLAYS
from components.neopixels import NEOPIXELS
from components.speaker import SUCCESS_SOUND, say, generate_speech

CHECKMARK_PATH = "./assets/checkmark.png"
PROPABILITY_COMMENT_ON_FAIL = 0.35

class LightsOut:
    def __init__(
            self,
            correct_glyph,
            incorrect_glyph: list[str],
            toggles: list[Button],
            displays: list[Display],
            introduction: str,
            on_fail: list[str],
            on_solve: str,
            on_solved_callback=None 
    ):
        self.correct_glyph = correct_glyph
        self.incorrect_glyph = incorrect_glyph
        self.buttons = toggles
        self.displays = displays
        self.running = True
        self.state = [False] * 4
        self.wiring = create_wiring()

        self.introduction = generate_speech(introduction)
        self.on_fail = [generate_speech(n) for n in on_fail]
        self.on_solve = generate_speech(on_solve)

        self.on_solved_callback = on_solved_callback

    def switch(self, switch_number):
        for i, b in enumerate(self.wiring[switch_number]):
            if b:
                self.state[i] = not self.state[i]
                self.update_display(i)
        if self.is_solved():
            self.handle_solved()
        else:
            if random.random() < PROPABILITY_COMMENT_ON_FAIL: #
                say(random.choice(self.on_fail))

    def update_display(self, display_number):
        if (self.state[display_number]):
            glyph = self.correct_glyph
        else:
            glyph = self.incorrect_glyph[display_number]
        self.displays[display_number].show_hieroglyph(glyph)

    def start(self):
        say(self.introduction)
        NEOPIXELS.start_continuous(0.7)
        for i in range(4):
            self.buttons[i].when_activated = lambda i=i: self.switch(i)
            self.buttons[i].when_deactivated = lambda i=i: self.switch(i)
            self.update_display(i)

    def stop(self):
        for i in range(4):
            self.displays[i].show_asset(CHECKMARK_PATH)
            self.buttons[i].when_activated = None
            self.buttons[i].when_deactivated = None

    def is_solved(self):
        return all(self.state)

    def handle_solved(self):
        if not self.is_solved():
            return
        self.stop()
        SUCCESS_SOUND.play()
        say(self.on_solve)
        NEOPIXELS.start_sine_blink_and_sleep((100, 255, 0), 6, 0.2)
        NEOPIXELS.start_continuous(0.3)

        if self.on_solved_callback:      
            self.on_solved_callback()


def create_wiring() -> list[list[bool]]:
    rng = random.Random()
    base = [
        [True, True, False, False],
        [True, True, True, False],
        [False, True, True, True],
        [False, False, True, True]
    ]

    # Apply the same permutation  to row and columns, so that diagnol stays the same (all true, such that each toggle
    # switch switches its own display)
    p = list(range(4))
    rng.shuffle(p)
    M = [[base[p[i]][p[j]] for j in range(4)] for i in range(4)]
    return M
