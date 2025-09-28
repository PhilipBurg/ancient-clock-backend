"""import random
from signal import pause

from gpiozero import Button

from components.buttons import TOGGLE_SWITCHES
from components.displays import Display, DISPLAYS


class IconSwitch:
    def __init__(self, correct_glyph, incorrect_glyph: list[str], toggles: list[Button], displays: list[Display]):
        self.correct_glyph = correct_glyph
        self.incorrect_glyph = incorrect_glyph
        self.buttons = toggles
        self.displays = displays
        self.running = True
        self.state = [False] * 4
        self.wiring = create_wiring()

        for i in range(4):
            self.buttons[i].when_activated = lambda i=i: self.switch(i)
            self.buttons[i].when_deactivated = lambda i=i: self.switch(i)
            self.update_display(i)

    def switch(self, switch_number):

        for i, b in enumerate(self.wiring[switch_number]):
            if b:
                self.state[i] = not self.state[i]
                self.update_display(i)

    def start


    def update_display(self, display_number):

        if (self.state[display_number]):
            glyph = self.correct_glyph
        else:
            glyph = self.incorrect_glyph[display_number]

        self.displays[display_number].show_hieroglyph(glyph)

def create_wiring() -> list[list[bool]]:
    rng = random.Random()

    # Base wiring (invertible over GF(2); each row toggles itself + at least one other)
    base = [
        [True, True, False, False],  # S1 -> D1, D2
        [True, True, True, False],  # S2 -> D1, D2, D3
        [False, True, True, True],  # S3 -> D2, D3, D4
        [False, False, True, True]  # S4 -> D3, D4
    ]

    # One random permutation applied to BOTH rows and columns
    p = list(range(4))
    rng.shuffle(p)

    # Permute rows and columns: M[i][j] = base[p[i]][p[j]]
    M = [[base[p[i]][p[j]] for j in range(4)] for i in range(4)]
    return M





i = IconSwitch('Owl', ['Lion', 'Man_standing', 'Elephant', 'Scarab'], TOGGLE_SWITCHES[:4], DISPLAYS[:4])
pause()
 """
 from signal import pause
from gpiozero import Button
from components.buttons import TOGGLE_SWITCHES
from components.displays import DISPLAYS

class IconSwitch:
    def __init__(self, correct_glyph, incorrect_glyph, toggles, displays):
        self.correct_glyph = correct_glyph
        self.incorrect_glyph = incorrect_glyph
        self.buttons = toggles
        self.displays = displays
        self.state = [False] * 4
        self.wiring = create_wiring()

        for i in range(4):
            self.buttons[i].when_activated = lambda i=i: self.switch(i)
            self.update_display(i)

    def switch(self, switch_number):
        for i, active in enumerate(self.wiring[switch_number]):
            if active:
                self.state[i] = not self.state[i]
                self.update_display(i)

    def update_display(self, display_number):
        if self.state[display_number]:
            glyph = self.correct_glyph
        else:
            glyph = self.incorrect_glyph[display_number]
        self.displays[display_number].show_hieroglyph(glyph)


def create_wiring():
    return [
        [False, True, False, False],
        [True, False, True, False],
        [False, True, False, True],
        [False, False, True, False],
    ]


i = IconSwitch("Scarab", ["Fish", "Goose", "Turtle", "Falcon"], TOGGLE_SWITCHES[:4], DISPLAYS[:4])
pause()
