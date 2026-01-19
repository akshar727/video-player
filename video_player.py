import time
import sys
import os
import subprocess
import pygame
sys.path.append(os.path.abspath("Driver"))
from WhisPlay import WhisPlayBoard

# Initialize board
board = WhisPlayBoard()
board.set_backlight(50)

# Initialize pygame mixer
pygame.mixer.init()

# Constants
FRAME_RATE = 29.94  # frames per second
FRAME_DURATION = 1 / FRAME_RATE  # seconds per frame
FRAME_PATH_TEMPLATE = "frames_raw/frame_{:04}.raw"
SOUND_FILE = "vid.wav"

# Load sound
def set_wm8960_volume_stable(volume_level: str):
    CARD_NAME = 'wm8960soundcard'
    CONTROL_NAME = 'Speaker'
    DEVICE_ARG = f'hw:{CARD_NAME}'

    command = ['amixer', '-D', DEVICE_ARG, 'sset', CONTROL_NAME, volume_level]

    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"INFO: Volume set to {volume_level}")
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to execute amixer: {e.stderr}", file=sys.stderr)
    except FileNotFoundError:
        print("ERROR: 'amixer' not found.", file=sys.stderr)

try:
    sound = pygame.mixer.music.load(SOUND_FILE)
    set_wm8960_volume_stable("121")
except Exception as e:
    print(f"Failed to load sound: {e}")
    sound = None

# Load raw frame
def load_raw_frame(path):
    with open(path, "rb") as f:
        return f.read()

# Play sound

pygame.mixer.music.play()

# Video playback loop
frame = 1
start_time = time.time()

while True:
    # Calculate the target frame based on elapsed audio time
    elapsed_time = pygame.mixer.music.get_pos() / 1000.0  # get_pos() returns ms
    target_frame = int(elapsed_time * FRAME_RATE) + 1  # +1 because frames start at 1
    # Only update frame if needed
    if target_frame > frame:
        frame = target_frame
        frame_file = FRAME_PATH_TEMPLATE.format(frame)
        print(f"Displaying frame {frame}: {frame_file}")
        if not os.path.exists(frame_file):
            print("Reached end of frames.")
            break

        image_data = load_raw_frame(frame_file)
        board.draw_image(0, 0, board.LCD_WIDTH, board.LCD_HEIGHT, image_data)
    
    # Small sleep to avoid 100% CPU usage
    time.sleep(0.001)
