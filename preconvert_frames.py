from PIL import Image
import os

INPUT_DIR = "frames"
OUTPUT_DIR = "frames_raw"

SCREEN_WIDTH = 240
SCREEN_HEIGHT = 240

os.makedirs(OUTPUT_DIR, exist_ok=True)

def convert_to_rgb565(img):
    img = img.convert("RGB")
    pixels = img.load()

    buf = bytearray(SCREEN_WIDTH * SCREEN_HEIGHT * 2)
    i = 0

    for y in range(SCREEN_HEIGHT):
        for x in range(SCREEN_WIDTH):
            r, g, b = pixels[x, y]
            rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
            buf[i] = (rgb565 >> 8) & 0xFF
            buf[i + 1] = rgb565 & 0xFF
            i += 2

    return buf
c = 0
input_frames = sorted(os.listdir(INPUT_DIR))
l = len(input_frames)
for filename in input_frames:
    if not filename.endswith(".png"):
        continue    
    if c % 50 == 0:
        print(f"Converting {c}/{l} frame: {filename}")

    img = Image.open(os.path.join(INPUT_DIR, filename))

    # --- resize + crop to fit screen ---
    img_ratio = img.width / img.height
    screen_ratio = SCREEN_WIDTH / SCREEN_HEIGHT

    if img_ratio > screen_ratio:
        new_height = SCREEN_HEIGHT
        new_width = int(new_height * img_ratio)
    else:
        new_width = SCREEN_WIDTH
        new_height = int(new_width / img_ratio)

    img = img.resize((new_width, new_height), Image.BILINEAR)

    left = (new_width - SCREEN_WIDTH) // 2
    top = (new_height - SCREEN_HEIGHT) // 2
    img = img.crop((left, top, left + SCREEN_WIDTH, top + SCREEN_HEIGHT))

    raw = convert_to_rgb565(img)

    out_name = filename.replace(".png", ".raw")
    with open(os.path.join(OUTPUT_DIR, out_name), "wb") as f:
        f.write(raw)
    c+=1

print("Done.")
