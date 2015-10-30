from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import sqlite3 as lite
import sys 

app = Flask('sybil')
app.config['DEBUG'] = False

@app.route("/") 

def print_rows():
    con = None
    
    try: 
        con = lite.connect('sybil.db')
        cur = con.cursor()

        cur.execute("SELECT count(*) FROM sybil")

        row = cur.fetchone()
        count = row[0]

        display = "{} entries in table".format(count)

    except lite.Error, e:
        display = "Error: {}".format(e.args[0])
    
    finally: 
        if con:
            con.close()

    return render_template('main.html', display=display)

if __name__ == "__main__":
    app.run(host='0.0.0.0')

