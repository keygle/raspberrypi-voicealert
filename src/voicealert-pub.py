#!/usr/bin/env python

import RPIO
import paho.mqtt.client as mqtt
from datetime import datetime


def setup():
    return {
        4:  'front-hendri',
        17: 'front-gate',
        22: 'big-tree',
        23: 'afdak',
        25: 'pool-wall'
    }

settings = {}


def main():
    print 'Pi voice alert v1.1.0 publisher started'
    global settings
    settings = setup()
    print settings

    register_gpio(settings)

    RPIO.wait_for_interrupts()
    RPIO.cleanup()


def register_gpio(pins):
    RPIO.setmode(RPIO.BCM)

    for pin in pins:
        print 'Adding interrupt callback for pin ' + str(pin) + ' publish to ' + pins[pin]
        RPIO.setup(pin, RPIO.IN, pull_up_down=RPIO.PUD_DOWN)
        RPIO.add_interrupt_callback(pin, channel_high, edge='rising', debounce_timeout_ms=1000)


def channel_high(pin, value):
    print 'Channel high: ' + str(pin) + ' value: ' + str(value)

    mqtt_client = mqtt.Client()
    mqtt_client.connect('192.168.1.18')

    global settings

    mqtt_client.publish('milligal801/sensors/alarm/' + settings[pin], str(datetime.now().isoformat()), 0, False)
    mqtt_client.disconnect()


if __name__ == '__main__':
    main()
