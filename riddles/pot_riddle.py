from time import sleep

from components.displays import DISPLAYS
from components.neopixels import NEOPIXELS
from components.speaker import SUCCESS_SOUND, say, generate_speech, start_music
from components.potentiometers import Potentiometers

CHECKMARK_PATH = "./assets/checkmark.png"
TOLERANCE = 5.0  # Toleranz für Zielwert (±5)

class PotRiddle:
    def __init__(self, introduction: str, on_fail: list[str], on_solve: str, target_sum: int, on_solved_callback=None):
        self.pots = Potentiometers()
        self.displays = DISPLAYS[8:11]  
        self.running = True
        self.target_sum = target_sum 

        self.introduction = generate_speech(introduction)
        self.on_fail = [generate_speech(n) for n in on_fail]
        self.on_solve = generate_speech(on_solve)

        # Callback, das beim Lösen aufgerufen wird
        self.on_solved_callback = on_solved_callback

    def start(self):
        """Blocking Loop – läuft so lange, bis das Rätsel gelöst ist."""
        start_music()
        say(self.introduction)
        NEOPIXELS.start_continuous(0.7)

        while self.running:
           
            values = [self.pots.get_percent(i) for i in range(3)]
            total = sum(values)

            # Werte auf den Displays anzeigen
            for i, v in enumerate(values):
                self.displays[i].show_text(f"{v:.0f}")

            # Check: Summe ~100
            if abs(total - self.target_sum) <= TOLERANCE:
                self.handle_solved()
                break

            sleep(0.3)

    def handle_solved(self):
        """Aktionen, wenn das Rätsel gelöst ist."""
        self.running = False
        for d in self.displays:
            d.show_asset(CHECKMARK_PATH)

        SUCCESS_SOUND.play()
        say(self.on_solve)
        NEOPIXELS.start_sine_blink_and_sleep((0, 255, 0), 1, 0.1)
        NEOPIXELS.start_continuous(0.3)
        

        # Callback triggern
        if self.on_solved_callback:
            self.on_solved_callback()

    def stop(self):
        self.running = False
