import random

from components.displays import DISPLAYS
from components.imagegenerator import HIEROGLYPHS

for i in DISPLAYS:
    key = random.choice(list(HIEROGLYPHS.keys()))
    i.show_hieroglyph(key)