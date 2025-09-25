import time
from components.speaker import generate_speech, say

print("Starte WAV-TTS-Test...")

# Erzwinge WAV statt MP3
filename = generate_speech("Hallo vom Raspberry Pi!", local=True)
print("Datei erzeugt:", filename)

say(filename)

# Wartezeit, damit Sound wirklich hörbar ist
time.sleep(5)

print("Fertig!")

