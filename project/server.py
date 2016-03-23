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
    # not sure we need this, but might be helpful later on
    logged = 0
    if 'Username' in session:
        logged = 1
    
        
    
    return render_template('index.html', SelectedMenu = 'Index')
    
    
@app.route('/index.html')
def dashIndex():
    print 'in hello world'
    
    return render_template('index.html', SelectedMenu = 'Index')

    
@app.route('/SuggestEvent.html')
def forms():
    print 'in forms'
    
    return render_template('SuggestEvent.html', SelectedMenu = 'SuggestEvent')
    
    
@app.route('/charts.html')
def charts():
    print 'in charts'
    
    return render_template('charts.html', SelectedMenu = 'Charts')
    
    
@app.route('/tables.html')
def tables():
    print 'in tables'
    
    return render_template('tables.html', SelectedMenu = 'Tables')
    
    
@app.route('/register.html', methods=['GET','POST'])
def register():
    print 'in register'
    
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
    
    rows = []
    if request.method == 'POST':
        
        #get this from form for checking if user already exists
        email = request.form['email']

        
        
        regQuery = cur.mogrify("SELECT Email FROM users WHERE Email = %s", (email,))
        print (regQuery)
        cur.execute(regQuery)
        
        rows=cur.fetchall()
        print ("rows")
        
        
        
        if (rows == []):
            check = request.form['password']
            check2 = request.form['pwConfirm']
            print check
            print check2
            
            if (check == check2):
                #dont have all users table datatypes, but we can work on that later
                regAddQuery = cur.mogrify("""INSERT INTO users (Username, Email, Password, Firstname, Lastname, Company, Address, City)
                    VALUES(%s, %s, crypt(%s, gen_salt('bf')), %s, %s, %s, %s, %s);""", (request.form['userName'],request.form['email'],request.form['password'],
                    request.form['firstName'],request.form['lastName'],request.form['comp'],request.form['address'],request.form['city']))
                print (regAddQuery)
                
                cur.execute(regAddQuery)
                print("after add execute")
                # commit to database
                conn.commit()
                print("person registered")
            else:
                print('passwords dont match, cant register')
            
        else:
            print ("email is taken so user exists")
            
    return render_template('register.html', SelectedMenu = 'Register')
    
@app.route('/AddEvent.html')
def addEvent():
    print 'in event addition'
    
    return render_template('AddEvent.html', SelectedMenu = 'AddEvent')
    
    
@app.route('/timeline.html')
def timeline():
    print 'in timeline'
    
    return render_template('timeline.html', SelectedMenu = 'Timeline')
    
    
    
@app.route('/login.html', methods=['GET','POST'])
def login():
    print 'in login'
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    if request.method == 'POST':
        print ("in if after POST")
        
        # get data from forms
        email = request.form['email']
        password = request.form['password']
        
        # mogrify query to prevent SQL injections
        loginQuery = cur.mogrify("select Username, Email from users WHERE Email = %s AND Password = crypt(%s, Password)" , (email, password,))
        
        # execute query
        cur.execute(loginQuery)
        print loginQuery
        
        # get result from query
        result = cur.fetchone()
        print result
        
        if result:
            print('logged in')
            print('name = ', result[0])
            
            # sets session username to first result from query
            # used for displaying username on webpages
            session['userName'] = result[0]
            print session['userName']
            
            # if logged in, redirect to home page
            return redirect(url_for('mainIndex'))
            
    return render_template('login.html', SelectedMenu = 'Login')
    
    
@app.route('/logout')
def logout():
    print('removing session variables')
    del session['userName']
    #print session['userName']
    #session['userName'].close()
    
    return redirect(url_for('mainIndex'))

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