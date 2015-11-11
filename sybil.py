# Requires Flask and SQLite3
from flask import Flask, url_for, render_template
import sqlite3, time

# Create the app
app = Flask('sybil')
app.config['DEBUG'] = False

# Index page
@app.route("/") 
def activity_chart():
    try: 
        # Connect to the db
        con = sqlite3.connect('sybil.db')
        cur = con.cursor()
        
        # Get all entries in the past 5 days and format the time as unix epoch time
        cur.execute("SELECT strftime('%s',time), active FROM sybil WHERE time BETWEEN datetime('now', '-5 days') AND datetime('now', 'localtime')")
        rows = cur.fetchall()

        # Form the data that will passed to the JS and HTML
        last_seen = 0
        data = []
        for row in rows:
            
            # [x,y] data pair where x is the number of milliseconds since epoch
            data.append( "[{},{}]".format(int(row[0])*1000, row[1]) )
            
            # About 10% can be attributed to uninteresting 'noise' (possibly Sybil rolling over but unlikely)
            if row[1] > 30.0:
                last_seen = int(row[0])

        data = "[" +','.join(data)+ "]"
        last_seen = time.strftime("%b %e, %I:%M%p", time.gmtime(last_seen)).capitalize().replace(", 0",", ")
        
        display = "Last active: {}".format( last_seen )

    except sqlite3.Error, e:
        display = "Error: {}".format(e.args[0])

    # Close the db connection    
    finally: 
        if con:
            con.close()

    return render_template('main.html', display=display, data=data)

# Start the app and make available to all
if __name__ == "__main__":
    app.run(host='0.0.0.0')
