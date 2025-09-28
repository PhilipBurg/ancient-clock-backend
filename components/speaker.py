import subprocess
import uuid
import wave
import os

import pygame
from piper import PiperVoice
from gtts import gTTS

os.sched_setaffinity(0, {0, 1})
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"

voice = PiperVoice.load("./voices/de_DE-thorsten-medium.onnx")

pygame.mixer.init()
SUCCESS_SOUND = pygame.mixer.Sound("./assets/success.mp3")

pygame.mixer.music.load("./assets/ancient_egypt.wav")

def start_music():
    pygame.mixer.music.set_volume(1.0)  #loudest
    pygame.mixer.music.play(-1)         

def stop_music():
    pygame.mixer.music.stop()

def lower_music():
    pygame.mixer.music.set_volume(0.3)  # little bit more quite when speaking

def restore_music():
    pygame.mixer.music.set_volume(1.0)

def generate_speech(text: str, local=False):

    if local:
        filename = f"./generated_speech/{uuid.uuid4()}.wav"
        with wave.open(filename, "wb") as wf:
            voice.synthesize_wav(text, wf)
    else:
        filename = f"./generated_speech/{uuid.uuid4()}.mp3"
        tts = gTTS(text=text, lang='de')
        tts.save(filename)

    return filename

def say(filename):
    lower_music()
    sound = pygame.mixer.Sound(filename)
    sound.play()
    while pygame.mixer.get_busy():  
        pygame.time.delay(100)
    restore_music()

def generate_and_say(text):
    say(generate_speech(text))
