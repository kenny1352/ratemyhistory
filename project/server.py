import os
import uuid
import psycopg2
import psycopg2.extras
import crypt, getpass, pwd
import time
from datetime import date
from flask import Flask, redirect, url_for,session, render_template, jsonify, request
#from flask.ext.socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

#socketio = SocketIO(app)

def connectToDB():
    #change connection to session db
    connectionString = 'dbname=ratemyhistory user=rateuser password=history host=localhost'
    print connectionString

    try:
        return psycopg2.connect(connectionString)
    except:
        print("Can't connect to database")


#CHANGE NAMESPACE TO WHAT WE DECIDE
# @socketio.on('connect', namespace='/')
# def makeConnection():
    
#     conn = connectToDB()
#     cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)        
        
        
        
        
@app.route('/')
def mainIndex():
    print 'in hello world'
    
    return render_template('index.html')
    
@app.route('/forms.html')
def formreply():
    return render_template('forms.html')
    

# start the server
if __name__ == '__main__':
        app.run(host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)        