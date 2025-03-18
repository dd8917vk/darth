from pathlib import Path
import time
import random
import os
from collections import deque
from io import StringIO
import sys
from gpiozero import Button
import threading

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

    # While the audio is playing, we keep the program running
    while pygame.mixer.music.get_busy():
        pygame.time.delay(100)  # Wait a little while checking for button press


def button_handler(button):
    """Thread to monitor the button press and hold event."""
    global should_exit
    button_held = False
    while True:
        if button.is_pressed:
            if not button_held:
                # Button has been pressed, so start monitoring for hold
                print("Button pressed, monitoring for hold.")
                button_held = True
                start_time = time.time()  # Start timer for hold time
        else:
            if button_held and time.time() - start_time >= 2:
                # Button was held for 2 seconds
                print("Button held for the required duration!")
                should_exit = True
                break
            button_held = False  # Reset if button was released before hold duration

        time.sleep(0.1)  # Delay to prevent too much CPU usage


def quit_program():
    print("Button held down! Exiting program...")
    sys.exit(0)


if __name__ == "__main__":
    should_exit = False

    # Initialize button
    button = Button(17, bounce_time=0.1)

    # Start the button press handler in a separate thread
    button_thread = threading.Thread(target=button_handler, args=(button,), daemon=True)
    button_thread.start()

    # Wait for the button press to start the audio
    print("Waiting for button press to start audio...")
    while True:
        if button.is_pressed:
            wav_files = get_wav_files()
            file_to_play = get_random_wav(wav_files)
            history.append(file_to_play)
            print(f"Playing {file_to_play}")
            play_sound(file_to_play)
            time.sleep(1)
            break  # Break out of the loop after playing the first file

    # Main loop will now continue after the first audio has finished playing
    while not should_exit:
        if button.is_pressed:
            wav_files = get_wav_files()
            file_to_play = get_random_wav(wav_files)
            history.append(file_to_play)
            print(f"Playing {file_to_play}")
            play_sound(file_to_play)
            time.sleep(1)

    quit_program()
