import RPi.GPIO as GPIO
import sys, time, datetime

time_up = 0
time_count = 0

def motion_detected(pin):
    global time_up
    global time_count

    if GPIO.input(pin):
        time_up = time.time()
    else:
        if time_up > 0:
            time_count += (time.time() - time_up)
            time_up = 0

PIR_PIN = 7

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

try:
    GPIO.add_event_detect(PIR_PIN, GPIO.BOTH, callback=motion_detected)
    while 1:
        time.sleep(30)
        print str(datetime.datetime.now()) + ": detected motion for " + str(time_count) + "s"
        time_count = 0 
except KeyboardInterrupt:
    print "\nQuitting ..."
except:
    print "Error ... "
finally:
    GPIO.cleanup()
sys.exit(1)
