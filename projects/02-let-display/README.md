# Project 02 — OLED Photo Converter

Turn a photo on your computer into a black-and-white image for a 128 × 64 SSD1306 OLED, then show it with an ESP32-S3 running MicroPython.

The computer does the image processing. It crops and resizes a selected photo, converts it to monochrome with dithering, and writes a small Python bitmap snippet. You paste that bitmap into the marked section of the ESP32 program. The ESP32 then draws it on the OLED.

This project deliberately uses a copy-and-paste step for the bitmap. The converter does not connect to the ESP32, change its firmware, or upload files over USB.

## What the project does

The OLED has 128 pixels across and 64 pixels down. It can show only two colors: each pixel is either black or white. Photos contain many colors and shades, so the converter prepares the image for this small display:

1. Opens a JPG, PNG, or another image format supported by Pillow.
2. Applies the photo's orientation metadata when available.
3. Center-crops the image to the OLED's 2:1 aspect ratio and resizes it to 128 × 64 pixels.
4. Converts it to grayscale, then uses Floyd–Steinberg dithering to represent shades with patterns of black and white pixels.
5. Packs the pixels into the layout expected by MicroPython's `framebuf.MONO_VLSB` mode.
6. Writes a `BITMAP = bytearray(...)` assignment that can be pasted into `main.py`.

The crop is centered, so the edges of a photo may be cut off. A close, well-lit subject with clear contrast usually reads best on the small display.

## Parts and software

### Hardware

- ESP32-S3 development board
- 128 × 64 SSD1306 monochrome OLED module with I2C interface
- USB data cable for programming and power
- Jumper wires
- A computer running Windows, macOS, or Linux

### Wiring

Connect the OLED to the ESP32-S3 as follows. The defaults match the original Project 2 example; change the pins in `main.py` if your board is wired differently.

| OLED pin | ESP32-S3 default | Purpose |
| --- | --- | --- |
| VCC | 3V3 | Power |
| GND | GND | Ground |
| SCL | GPIO 9 | I2C clock |
| SDA | GPIO 8 | I2C data |

Use the voltage supported by your OLED module; 3.3 V is the usual choice for ESP32 projects. The program uses I2C address `0x3C`. If your OLED uses `0x3D`, change `OLED_ADDRESS` in `main.py`.

### Computer software

- Python 3.9 or newer
- Pillow, installed from this project's `requirements.txt`

The ESP32 must run MicroPython to run `main.py`. The converter itself runs on your computer and does not require MicroPython or `mpremote`.

## Project files

```text
02-let-display/
├── README.md              Project guide
├── requirements.txt       Computer-side Python dependency
├── convert_photo.py       Photo conversion program for your computer
├── main.py                ESP32 program; paste the generated bitmap here
├── ssd1306.py             MicroPython SSD1306 I2C display driver
├── assets/                Place source photos here if you want
├── output/
│   └── photo_bitmap.py    Generated bitmap snippet
└── examples/              Optional examples and previews
```

`letdisplay.py` is the original hard-coded bitmap example. The reusable workflow described below uses `convert_photo.py` and `main.py`.

## 1. Set up the computer converter

Open a terminal in this project folder. In VS Code, use **Terminal → New Terminal**, then change to the folder. For example:

```powershell
cd "D:\Desktop\projects\esp32-projects-lab\projects\02-let-display"
```

Install Pillow:

```powershell
py -m pip install -r requirements.txt
```

If Windows says `py` is not recognized, install Python from [python.org](https://www.python.org/downloads/) and reopen the terminal. On a system where the Python command is `python` instead, use `python -m pip install -r requirements.txt` and `python convert_photo.py` in the commands below.

## 2. Convert a photo

To open a file picker, run:

```powershell
py convert_photo.py
```

Choose an image file. The converter writes the bitmap code to:

```text
output/photo_bitmap.py
```

You can also provide the photo's path directly:

```powershell
py convert_photo.py "D:\Downloads\portrait.jpg"
```

Paths with spaces should be surrounded by quotation marks. To choose a different output file:

```powershell
py convert_photo.py "D:\Downloads\portrait.jpg" --output output\family_photo.py
```

The output file contains only the Python assignment for `BITMAP`. It represents 1,024 bytes: 128 × 64 pixels, with one bit per pixel. The project uses `bytearray` so MicroPython can use the data as a framebuffer.

### If conversion fails

- **Image file does not exist:** check the path and spelling. In File Explorer, use **Copy as path** and put the path in quotes.
- **Unsupported or damaged image:** try opening and re-saving it as a JPG or PNG.
- **Pillow is missing:** run `py -m pip install -r requirements.txt` from this project folder.
- **No file picker appears:** pass the image path directly as shown above.

## 3. Paste the bitmap into `main.py`

Open `output/photo_bitmap.py`. Copy the entire assignment, starting at `BITMAP = bytearray((` and ending at its matching closing `))`:

```python
BITMAP = bytearray((
    ... generated byte values ...
))
```

Open this project's `main.py`. Find the clearly marked block:

```python
# --- GENERATED PHOTO BITMAP ---
# Replace the empty assignment with the complete BITMAP assignment from
# output/photo_bitmap.py. Keep the generated code inside these comment markers.
BITMAP = bytearray()
# --- END GENERATED PHOTO BITMAP ---
```

Replace only the `BITMAP = bytearray()` placeholder line with the copied assignment. Keep both marker comments in place. For example, the section should look like this after pasting:

```python
# --- GENERATED PHOTO BITMAP ---
# Replace the empty assignment with the complete BITMAP assignment from
# output/photo_bitmap.py. Keep the generated code inside these comment markers.
BITMAP = bytearray((
    255, 191, 127, ...
))
# --- END GENERATED PHOTO BITMAP ---
```

Use all generated numbers; `...` above is only an illustration. Do not paste the bitmap into `ssd1306.py` or leave it in a separate `photo_bitmap.py` file. `main.py` contains the display setup and needs the bitmap assignment directly in its marked section.

The `len(BITMAP)` check in `main.py` expects exactly 1,024 bytes. If the placeholder is still empty or some generated values are missing, the program stops with an explanatory error instead of trying to draw an invalid image.

## 4. Save and run it on the ESP32

The ESP32 needs MicroPython firmware installed. The board should be connected over USB and appear as a MicroPython device in your editor.

Using Thonny:

1. Connect to the ESP32's MicroPython interpreter.
2. Open this project's `ssd1306.py` on your computer and choose **File → Save as… → MicroPython device**. Save it at the device root as `ssd1306.py`.
3. Open this project's edited `main.py` and save it to the device root as `main.py`.
4. Press **Run** to run the current file. To show the photo automatically after power-up, leave the file named `main.py` on the device and press **RESET**.

Using another MicroPython editor, copy the two files to the board's top-level filesystem as `ssd1306.py` and `main.py`, then run `main.py` or reset the board.

The bitmap snippet is plain MicroPython source. The manual copy step transfers it into `main.py`; you do not need to copy `output/photo_bitmap.py` to the board.

## 5. Adjust the display settings

At the top of `main.py`, these values configure the screen and I2C pins:

```python
WIDTH = 128
HEIGHT = 64
OLED_SCL_PIN = 9
OLED_SDA_PIN = 8
OLED_I2C_BUS = 0
OLED_ADDRESS = 0x3C
```

The driver initializes I2C at 100 kHz. If the display stays blank, check the power and ground, confirm the SCL/SDA pins match your wiring, and verify the OLED address. Some modules use `0x3D`. The display driver and bitmap format are for a 128 × 64 SSD1306; other display sizes or controller chips need corresponding code changes.

## How the bitmap is stored

The OLED uses a monochrome framebuffer. `convert_photo.py` packs eight vertical pixels into each byte in the order expected by `framebuf.MONO_VLSB`; set bits represent lit (white) pixels. `main.py` creates a framebuffer from the pasted bytearray, copies it to the SSD1306 buffer, and calls `oled.show()` to send it to the display.

This keeps image processing on the computer and the ESP32 code small. Every new photo only requires running the converter again and replacing the bitmap assignment in `main.py`.
