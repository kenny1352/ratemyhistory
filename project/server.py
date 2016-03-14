import os
import uuid
import psycopg2
import psycopg2.extras
import crypt, getpass, pwd
from flask import Flask,render_template, redirect, url_for,session, jsonify, request
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
        

print 'before app route'
#for displaying html pages        
@app.route('/index.html')
def mainIndex():
    print 'in hello world'
    
    return render_template('index.html')
    
    
@app.route('/forms.html')
def forms():
    print 'in forms'
    
    return render_template('forms.html')
    
    
@app.route('/charts.html')
def charts():
    print 'in charts'
    
    return render_template('charts.html')
    
    
@app.route('/tables.html')
def tables():
    print 'in tables'
    
    return render_template('tables.html')
    
    
#probably remove these later, but added them just to see what things could look like
@app.route('/bootstrap-elements.html')
def bootstrap():
    print 'in tables'
    
    return render_template('bootstrap-elements.html')
    
@app.route('/bootstrap-grid.html')
def bootstrap2():
    print 'in tables'
    
    return render_template('bootstrap-grid.html')

# start the server
if __name__ == '__main__':
        app.run(host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)    