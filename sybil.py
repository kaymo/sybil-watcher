from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import sqlite3 as lite
import sys, datetime, time 

app = Flask('sybil')
app.config['DEBUG'] = False

@app.route("/") 

def print_rows():
    con = None
    
    try: 
        con = lite.connect('sybil.db')
        cur = con.cursor()

        cur.execute("SELECT strftime('%s',time), active FROM sybil WHERE time BETWEEN datetime('now', '-28 days') AND datetime('now', 'localtime')")

        rows = cur.fetchall()

        last_seen = 0
        data = []
        for row in rows:
            active = row[1]
            if row[1] > 1000.0:
                active = 0.0
            data.append( "[{},{}]".format(int(row[0])*1000, active) )
            if active > 0.0:
                last_seen = row[0]
        data = "[" +','.join(data)+ "]"
        display = "Sybil last spotted at {}".format(datetime.datetime.fromtimestamp(int(last_seen)))
    except lite.Error, e:
        display = "Error: {}".format(e.args[0])
    
    finally: 
        if con:
            con.close()

    return render_template('main.html', display=display, data=data)

if __name__ == "__main__":
    app.run(host='0.0.0.0')

