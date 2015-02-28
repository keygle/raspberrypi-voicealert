#!/usr/bin/env python

import paho.mqtt.client as mqtt
import pygame
import glob


mqtt_server = '192.168.1.18'
mqtt_topic_filter = 'milligal801/sensors/alarm/+'
sounds = {}


def main():
    print 'Pi voice alert v1.1.0 subscriber started'

    print 'Connecting to MQTT broker: ' + mqtt_server
    mqtt_client = mqtt.Client()
    mqtt_client.on_message = on_message
    mqtt_client.connect(mqtt_server)
    print 'Connected'

    mqtt_client.subscribe(mqtt_topic_filter)
    print 'Subscribed to: [' + mqtt_topic_filter + '] ...'

    # Initialise sounds

    print "Initialising mixer..."
    mixer = pygame.mixer
    mixer.init()

    sound_files = glob.glob("sounds/*.ogg")

    print 'Load sound files:'
    for sound_file in sound_files:
        filename = sound_file[7:-4]
        print ' - ' + sound_file + ' [' + filename + ']'
        sounds[filename] = mixer.Sound(sound_file)

    mixer.Sound("sounds/startup.wav").play()

    mqtt_client.loop_forever()


def on_message(client, userdata, msg):
    print 'Message received topic = ' + str(msg.topic) + ', payload = ' + msg.payload
    alarm_name = msg.topic[len(mqtt_topic_filter) - 1:]
    sounds[alarm_name].play(1)


if __name__ == '__main__':
    main()
