import RPi.GPIO as GPIO
import sys, time, datetime
import sqlite3 as lite

INTERVAL = 300

# Connect to database
con = None
cur = None
try: 
    con = lite.connect('sybil.db')
    cur = con.cursor()

except lite.Error, e:
    print "Error: {}".format(e.args[0])

# Time trackers
time_up = 0.0
time_count = 0.0
app_start = time.time()

# Motion callback (rising and falling events)
def motion_detected(pin):
    global time_up
    global time_count

    if GPIO.input(pin):
        time_up = time.time()
    elif time_up > app_start:
        time_count += (time.time() - time_up)
        time_up = 0.0

# Pi setup
PIR_PIN = 7

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

# Start detection
try:
    # Kick off event thread
    GPIO.add_event_detect(PIR_PIN, GPIO.BOTH, callback=motion_detected)
    
    # Infinite loop to summarise the motion detected
    while 1:
        time.sleep(INTERVAL)
        
        # If motion is currently detected then add to interval total
        if time_up > app_start:
            time_count += time.time() - time_up
            time_up = time.time()
        
        # Add to the db and print to console
        if cur and (time_count < (INTERVAL+10)):
            cur.execute('INSERT INTO sybil (active) VALUES (?)', (round(time_count,3),) )
            con.commit()
		
        print str(datetime.datetime.now()) + ": detected motion for " + str(round(time_count,3)) + "s"
        
        # Reset for the next interval
        time_count = 0.0

except lite.Error, e:
    print "Error: {}".format(e.args[0])

except KeyboardInterrupt:
    print "\nQuitting ..."

finally:
    # Pi cleanup
    GPIO.cleanup()

    # Close db connection
    if con:
        con.close()
