import RPIO
import time
import pygame
import glob


def getSoundFiles():
  return glob.glob("channel*.ogg")


def parseChannelNo(fname):
  channelNo = fname[7:][:-4]
  return int(channelNo)


def buildDefinitions(files):
  defs = {}
  for file in files:
     print "Parsing: " + file
     channelNo = parseChannelNo(file)
     print "Channel: " + str(channelNo)
     defs[channelNo] = file
  return defs


def chan_high(channel, value):
  print "HIGH: " + str(channel) + " value: " + str(value) 
  global sounds
  effect = sounds[channel]
  effect.play(1)


files  = getSoundFiles()
defs   = buildDefinitions(files)

# Initialise sounds
sounds = {}
print "Initialising mixer..."
mixer = pygame.mixer;
mixer.init()

for key, value in defs.iteritems():
  sounds[key] = mixer.Sound(value)
  
sndDone = mixer.Sound("done.wav")
mixer.Sound("startup.wav").play()

print "Sounds loaded"

# Register GPIO events
RPIO.setmode(RPIO.BCM)

for key in defs:
  print "Adding event detect for: " + str(key)
  RPIO.setup(key, RPIO.IN, pull_up_down=RPIO.PUD_DOWN)
  RPIO.add_interrupt_callback(key, chan_high, edge='rising', debounce_timeout_ms=1000)

RPIO.wait_for_interrupts()

RPIO.cleanup()

sndDone.play(2)
time.sleep(2) # wait for sound clip to finish
