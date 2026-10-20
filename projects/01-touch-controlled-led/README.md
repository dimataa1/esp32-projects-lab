# Project 01 — Touch-Controlled LED

**Category:** Embedded Systems / Electronics  
**Platform:** ESP32-S3  
**Language:** MicroPython  
**Status:** Working prototype

## Overview

This project implements a touch-controlled LED using an ESP32-S3 microcontroller and a TTP223 capacitive touch sensor.

When the sensor detects a touch, its digital output changes state and the ESP32 turns on an LED. When the touch is released, the LED turns off.

The project introduces GPIO input/output, digital signals, breadboard prototyping, and basic embedded programming.

## Objectives

- Read a digital signal from a capacitive touch sensor.
- Control an LED using a microcontroller GPIO output.
- Understand the relationship between hardware connections and software.
- Build a reproducible, documented electronics prototype.

## Hardware Components

| Component | Purpose |
|---|---|
| ESP32-S3 | Main microcontroller |
| TTP223 touch sensor | Detects touch |
| LED | Visual output |
| 220–330 Ω resistor | Limits LED current |
| Breadboard and jumper wires | Circuit assembly |
| USB data cable | Programming and power |

## Wiring

| Component pin | ESP32-S3 connection |
|---|---|
| Sensor GND | GND |
| Sensor VCC | 3V3 |
| Sensor IO | GPIO 4 |
| LED anode (+) | GPIO 5 through a resistor |
| LED cathode (−) | GND |

**Note:** Confirm the GPIO labels on your specific ESP32-S3 board before wiring.

## How It Works

1. The ESP32 configures GPIO 4 as a digital input.
2. The touch sensor outputs a digital signal when touched.
3. The program reads the sensor state in a continuous loop.
4. GPIO 5 drives the LED according to the sensor state.

## Software

The firmware is written in MicroPython and can be executed using Thonny.

```python
from machine import Pin
from time import sleep_ms

touch = Pin(4, Pin.IN)
led = Pin(5, Pin.OUT)

while True:
    led.value(touch.value())
    sleep_ms(20)
```

## Testing and Results

Record actual observations before publishing results.

- [ ] LED turns on when the sensor is touched.
- [ ] LED turns off when the sensor is released.
- [ ] Circuit works after restarting the ESP32.
- [ ] Connections and component values are documented.

### Test Metrics

| Metric | Result |
|---|---|
| Total test attempts | To be measured |
| Successful detections | To be measured |
| Missed detections | To be measured |
| Response time | To be measured |

## Challenges and Lessons Learned

Document any problems encountered during assembly, serial-port configuration, sensor behavior, or wiring. Explain how each issue was diagnosed and resolved.

## Future Improvements

- Add software debouncing or filtering if required.
- Add a mode that toggles the LED on each touch.
- Display sensor state on an OLED.
- Log touch events and analyze response time.
- Integrate the sensor into a larger access-control prototype.

## Media

Check the media folder.

## Author
Dimitar Dimov
Developed as part of an ongoing ESP32 embedded-systems learning portfolio.
