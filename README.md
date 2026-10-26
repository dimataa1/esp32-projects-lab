# ESP32 Projects Lab

A growing collection of small, hands-on embedded systems projects built around the ESP32 family. The lab is a place to learn by building: each project combines a circuit, MicroPython code, and notes that make the build easier to understand and reproduce.

The current projects use an ESP32-S3 and MicroPython. Projects are kept in their own numbered folders so their code, wiring notes, dependencies, and media stay together.

## Projects

| Project | What it does | Main ideas | Folder |
| --- | --- | --- | --- |
| **01 — Touch-Controlled LED** | A TTP223 capacitive touch sensor controls an LED connected to an ESP32-S3. | GPIO input and output, digital signals, simple circuits | [`projects/01-touch-controlled-led`](projects/01-touch-controlled-led/) |
| **02 — OLED Photo Converter** | A computer-side tool converts a photo into a 128 × 64 monochrome bitmap snippet. Paste the snippet into the ESP32's `main.py` to display the photo on an SSD1306 OLED. | I2C, OLED framebuffers, image resizing, grayscale conversion, dithering, bitmap packing | [`projects/02-let-display`](projects/02-let-display/) |
| **03 — Smart Distance Meter** | An HC-SR04 ultrasonic sensor measures distance, and an SSD1306 OLED shows the result and a close-range warning. | Trigger/echo pulses, time-of-flight measurement, I2C, voltage dividers | [`projects/03-smart-distance-meter`](projects/03-smart-distance-meter/) |

Each project has its own README with the parts, wiring, setup, and run instructions. Start with the README inside the project folder you want to build.

## Repository layout

```text
esp32-projects-lab/
├── README.md
└── projects/
    ├── 01-touch-controlled-led/
    │   ├── README.md
    │   ├── touch_sensor_led.py
    │   └── media/
    ├── 02-let-display/
    │   ├── README.md
    │   ├── convert_photo.py
    │   ├── main.py
    │   ├── ssd1306.py
    │   ├── requirements.txt
    │   ├── assets/
    │   ├── examples/
    │   ├── media/
    │   └── output/
    └── 03-smart-distance-meter/
        ├── README.md
        ├── main.py
        ├── scheme.png
        └── media/
```

## Getting started

### Hardware and MicroPython projects

1. Check the project's README for its parts list and pin assignments.
2. Connect the ESP32 board to your computer with a USB data cable.
3. Install MicroPython firmware for your specific ESP32 board if it is not already installed.
4. Open the project in an editor that supports MicroPython, such as Thonny.
5. Copy the project's `.py` files to the board as described in that project's README, then run the entry-point file.

Pin numbers and board layouts can differ. Check the labels on your board and follow the project-specific wiring notes before connecting components.

### Project 02 computer-side converter

Project 02 also includes a program that runs on your computer. From its folder, install its Python dependency with:

```powershell
py -m pip install -r requirements.txt
```

Then run the converter with a photo path, or launch its file picker:

```powershell
py convert_photo.py "C:\path\to\photo.jpg"
```

The converter writes a bitmap code snippet. Copy it into the marked section of Project 02's `main.py` before saving that file to the ESP32. See the [Project 02 README](projects/02-let-display/README.md) for the full process.

### Project 03 distance meter

Project 03 uses an HC-SR04 ultrasonic sensor and a 128 × 64 SSD1306 OLED. Its README includes the GPIO map, ECHO voltage-divider wiring, explanation of the distance calculation, and instructions for running the MicroPython program. See the [Project 03 README](projects/03-smart-distance-meter/README.md).

## Learning and contributing

These projects are intended to be understandable and buildable starting points. As the lab grows, each project can document:

- The goal and how the circuit works
- A parts list and wiring diagram
- How to install dependencies and run the code
- Observed behavior, troubleshooting notes, and possible extensions
- Photos or videos from the build

When adding a project, give it the next number, create a dedicated folder under `projects/`, and include a project README with its hardware and software instructions. Keep project-specific dependencies and media in that folder.

## Author

Dimitar Dimov — an ongoing ESP32 and embedded systems learning portfolio.
