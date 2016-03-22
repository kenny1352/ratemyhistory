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
    connectionString = 'dbname=ratemyhistory user=assist password=assist host=localhost'
    print connectionString

    try:
        print("connected!")
        return psycopg2.connect(connectionString)
    except:
        print("Can't connect to database")


#CHANGE NAMESPACE TO WHAT WE DECIDE
# @socketio.on('connect', namespace='/')
# def makeConnection():
    
#     conn = connectToDB()
#     cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)        
        
print ("before app route")


#for displaying html pages        
@app.route('/')
def mainIndex():
    print 'in hello world'
    
    return render_template('index.html', SelectedMenu = 'Index')
    
    
@app.route('/index.html')
def dashIndex():
    print 'in hello world'
    
    return render_template('index.html', SelectedMenu = 'Index')

    
@app.route('/SuggestEvent.html')
def forms():
    print 'in forms'
    
    return render_template('SuggestEvent.html', SelectedMenu = 'SuggestEvent')
    
    
@app.route('/charts')
def charts():
    print 'in charts'
    
    return render_template('charts.html', SelectedMenu = 'Charts')
    
    
@app.route('/tables')
def tables():
    print 'in tables'
    
    return render_template('tables.html', SelectedMenu = 'Tables')
    
    
@app.route('/register.html')
def register():
    print 'in register'
    
    return render_template('register.html', SelectedMenu = 'Register')
    
@app.route('/AddEvent.html')
def addEvent():
    print 'in event addition'
    
    return render_template('AddEvent.html', SelectedMenu = 'AddEvent')
    
@app.route('/login.html', methods=['GET','POST'])
def login():
    print 'in login'
    
    return render_template('login.html', SelectedMenu = 'Login')
    
#probably remove these later, but added them just to see what things could look like
@app.route('/bootstrap-elements')
def bootstrap():
    print 'in tables'
    
    return render_template('bootstrap-elements.html', SelectedMenu = 'Bootstrap-elements')
    
@app.route('/bootstrap-grid')
def bootstrap2():
    print 'in tables'
    
    return render_template('bootstrap-grid.html', SelectedMenu = 'Bootstrap-grid')

# start the server
if __name__ == '__main__':
        app.run(host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)