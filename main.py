from pathlib import Path
import time
import random
import os
from collections import deque
from io import StringIO
import sys
# os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

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
    # Initialyze pygame mixer for audio
    pygame.mixer.init()
    # file_path = Path.cwd() / "luke_4_8.wav"
    # print(file_path)
    pygame.mixer.music.load(str(the_wav_file))
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.delay(100)


if __name__ == "__main__":
    start = True
    while start:
        user_input = str(
            input("Would you like to play the next audio file? y or n: "))
        if user_input == "n":
            play_sound(Path.cwd() / "be_with_you.wav")
            start = False
            break
        wav_files = get_wav_files()
        file_to_play = get_random_wav(wav_files)
        history.append(file_to_play)
        print(f"Playing {file_to_play}")
        play_sound(file_to_play)
        time.sleep(1)
