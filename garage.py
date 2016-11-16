import thread, time, getopt, sys
import RPi.GPIO as GPIO
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

TEST_MODE = False

doorSensor = 26
motionSensor = 12
doorRelay = 13
doorOpenSensor = 4
kitchenDoorSensor = 5

doorIsOpen = False
door2IsOpen = False
kitchenIsOpen = False
motionDetected = False

GPIO.setup(doorRelay, GPIO.OUT)
GPIO.setup(doorSensor, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(doorOpenSensor, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(kitchenDoorSensor, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(motionSensor, GPIO.IN, GPIO.PUD_DOWN)

# TODO:
# Have garage.py understand door state (keep track of variables)
#  for like when the button is pressed and it's closed, it goes to 'opening'
# If Opening and button pressed, should it go

def pokeDoorRelay(state):
  if not TEST_MODE:
    GPIO.output(doorRelay, state)
  else:
    print("Door Relay simulated:", state)
  return;


def sendDoorSignal():
  print("Sending door signal")
  # Enable the relay
  pokeDoorRelay(1)

  # Wait a bit before closing relay
  time.sleep(0.5)

  # Disable the relay
  pokeDoorRelay(0)
  print("Door signal complete")
  return;


def isDoorOpen():
  return GPIO.input(doorSensor) == GPIO.HIGH;

def isDoor2Open():
  return GPIO.input(doorOpenSensor) == GPIO.HIGH;

def isKitchenOpen():
  return GPIO.input(kitchenDoorSensor) == GPIO.HIGH;

def isMotion():
  return GPIO.input(motionSensor) == GPIO.HIGH;

 
def monitorDoorStatus():
  global doorIsOpen
  global door2IsOpen
  global kitchenIsOpen
  while True:
    # Door sensor #1 
    if isDoorOpen() and doorIsOpen == False:
      print("Door #1 has been opened")
      doorIsOpen = True  
    elif not isDoorOpen() and doorIsOpen:
      print("Door #1 has been closed")
      doorIsOpen = False

    # Door sensor #2 
    if isDoor2Open() and door2IsOpen == False:
      print("Door #2 has been opened")
      door2IsOpen = True  
    elif not isDoor2Open() and door2IsOpen:
      print("Door #2 has been closed")
      door2IsOpen = False

    # Kitchen Door sensor
    if isKitchenOpen() and kitchenIsOpen == False:
      print("Kitchen has been opened")
      kitchenIsOpen = True  
    elif not isKitchenOpen() and kitchenIsOpen:
      print("Kitchen has been closed")
      kitchenIsOpen = False
    time.sleep(0.5)
  return

def monitorMotion():
  global motionDetected
  start = time.time()
  while True:
    if isMotion() and not motionDetected:
      elapsed = time.time() - start
      print("MOTION")
      print elapsed
      motionDetected = True
      pokeDoorRelay(1)
      start = time.time()
    elif not isMotion() and motionDetected:
      elapsed = time.time() - start
      print("NO MOTION", elapsed)
      motionDetected = False
      pokeDoorRelay(0)
      start = time.time()
    time.sleep(0.1)
  return
 
def sendDoorEvent():
    return

def sendMotionEvent():
    return

# Sends a POST event to the SmartThings hub
def sendHubEvent():
    return

@app.route('/trigger', methods=['POST'])
def triggerDoor():

    status = {
        'doorState' : "Closing..." if isDoorOpen() else "Opening..."
    }
    sendDoorSignal()

    return jsonify(status)

@app.route('/status')
def getStatus():
    status = {
        'isDoorOpen': isDoorOpen(),
        'motionDetected': isMotion()
    }

    return jsonify(status)

def runService():
  app.run(host='0.0.0.0', port=80, debug=True, use_reloader=False)
  return


if __name__ == "__main__":
  try:
     opts, args = getopt.getopt(sys.argv[1:],"t")
  except getopt.GetoptError:
     print 'Usage: garage.py -t'
     sys.exit(2)
  for opt, arg in opts:
     if opt == '-t':
       TEST_MODE = True


  doorIsOpen = False

  # Set the door state at startup
  doorIsOpen = isDoorOpen()
  door2IsOpen = isDoor2Open()
  kitchenIsOpen = isKitchenOpen()

  # Reset the relay to be off at startup
  pokeDoorRelay(0)

  try:
    thread.start_new_thread( monitorDoorStatus, () )
    thread.start_new_thread( monitorMotion, () )
    thread.start_new_thread( runService, () )
  except Exception, errtxt:
     print errtxt
  print "derp"

  while True:
    time.sleep(1)
