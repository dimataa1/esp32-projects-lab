
from machine import Pin, I2C, time_pulse_us
from time import sleep, sleep_us
import ssd1306

# OLED: I2C connection
i2c = I2C(0, scl=Pin(6), sda=Pin(7), freq=100000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# HC-SR04 pins
trig = Pin(4, Pin.OUT)
echo = Pin(5, Pin.IN)

trig.value(0)
sleep(0.5)


def measure_distance():
    # Send a 10-microsecond trigger pulse
    trig.value(0)
    sleep_us(2)
    trig.value(1)
    sleep_us(10)
    trig.value(0)

    try:
        duration = time_pulse_us(echo, 1, 30000)

        if duration < 0:
            return None

        # Sound travels to the object and back
        distance = duration * 0.0343 / 2
        return distance

    except OSError:
        return None


while True:
    distance = measure_distance()

    oled.fill(0)
    oled.text("DISTANCE METER", 0, 0)
    oled.hline(0, 12, 128, 1)

    if distance is None:
        oled.text("No echo found", 0, 25)
        oled.text("Check sensor", 0, 40)
    else:
        oled.text("Distance:", 0, 22)
        oled.text("{:.1f} cm".format(distance), 0, 38)

        if distance < 10:
            oled.text("TOO CLOSE!", 0, 53)
        else:
            oled.text("Measuring...", 0, 53)

    oled.show()
    sleep(0.2)
