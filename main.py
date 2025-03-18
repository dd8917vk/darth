from pathlib import Path
import time
import random
import os
from collections import deque
from io import StringIO
import sys
from gpiozero import Button

history = deque(maxlen=5)


def get_wav_files():
    # Get wav files
    directory = Path("./")
    wav_files = [f for f in directory.glob("*.wav")]
    if len(wav_files) < 6:
        raise ValueError(
            "There must be at least six WAV files to properly track history")
    return wav_files


def get_random_wav(wav_files):
    while True:
        choice = random.choice(wav_files)
        if choice not in history:
            return choice


def play_sound(the_wav_file):
    # Need sys.stdout to suppress pygame output
    sys.stdout = StringIO()
    import pygame
    # Set stdout back to normal
    sys.stdout = sys.__stdout__
    # Initialize pygame mixer for audio
    pygame.mixer.init()
    pygame.mixer.music.load(str(the_wav_file))
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        button.when_held = quit_program
        pygame.time.delay(100)


def quit_program():
    print("Button held down! Exiting program...")
    sys.exit(0)


if __name__ == "__main__":
    button = Button(17, hold_time=2, bounce_time=0.1)  # Adjust GPIO pin as needed and set hold_time for the duration to hold
      # Define what happens when the button is held

    while True:
        if button.is_pressed:
            wav_files = get_wav_files()
            file_to_play = get_random_wav(wav_files)
            history.append(file_to_play)
            print(f"Playing {file_to_play}")
            play_sound(file_to_play)
            time.sleep(1)
