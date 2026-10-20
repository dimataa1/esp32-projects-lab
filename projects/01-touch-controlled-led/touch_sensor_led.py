from machine import Pin
from time import sleep_ms

touch = Pin(1, Pin.IN)
led = Pin(5, Pin.OUT)

while True:
    led.value(touch.value())
    sleep_ms(20)