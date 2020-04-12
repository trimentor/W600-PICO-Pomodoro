"""
A simple pomodoro timer.
Work on a given task - focused - for 25 minutes followed by a five minute break.
Each fifth iteration the break will be 30 minutes, because you deserve it!
"""
from machine import Pin
from sys import exit
from utime import sleep

program_button  = Pin(Pin.PB_07, Pin.IN, Pin.PULL_UP)

progress_leds = [
    Pin(Pin.PB_13, Pin.OUT, Pin.PULL_FLOATING),
    Pin(Pin.PB_14, Pin.OUT, Pin.PULL_FLOATING),
    Pin(Pin.PB_15, Pin.OUT, Pin.PULL_FLOATING),
    Pin(Pin.PB_16, Pin.OUT, Pin.PULL_FLOATING),
    Pin(Pin.PB_17, Pin.OUT, Pin.PULL_FLOATING)
]

break_leds = [
    Pin(Pin.PB_18, Pin.OUT, Pin.PULL_FLOATING),
    Pin(Pin.PB_06, Pin.OUT, Pin.PULL_FLOATING)
]

def blink(led, seconds=3):
    sec = 0
    while sec < seconds:
        led.value(0)
        sleep(.5)
        led.value(1)
        sleep(.5)
        led.value(0)
        sec += 1

def start_pomodoro():
    for led in progress_leds + break_leds:
        led.value(0)

    for led in progress_leds:
        sleep(5 * 60)
        led.value(1)

def start_short_break():
    break_leds[0].value(1)

    for led in progress_leds:
        sleep(1 * 60)
        led.value(0)

    break_leds[0].value(0)

def start_long_break():
    break_leds[1].value(1)

    for led in progress_leds:
        sleep(6 * 60)
        led.value(0)

    break_leds[1].value(0)

work_cycles = 0
while True:
    # State: INITIAL

    # Drop to REPL when button is pressed
    if (work_cycles == 0 and not program_button.value()):
        print('Dropping to REPL')
        blink(break_leds[0])
        exit()

    # State: POMODORO
    start_pomodoro()
    work_cycles += 1

    if (work_cycles % 5 == 0):
        start_long_break()
    else:
        start_short_break()

    # State: SIGNALING

    # Wait until the button is pressed to start the next cycle
    while program_button.value():
        for led in break_leds:
            blink(led, 1)
