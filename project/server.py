import os
import uuid
import psycopg2
import psycopg2.extras
import crypt, getpass, pwd
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date
from flask import Flask, redirect, url_for,session, render_template, jsonify, request
from flask.ext.socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)

def connectToDB():
    #change connection to session db
    connectionString = 'dbname=ratemyhistory user=assist password=assist host=localhost'
    print connectionString

    try:
        print("connected!")
        return psycopg2.connect(connectionString)
    except:
        print("Can't connect to database")

       


@socketio.on('connect', namespace='/iss')
def makeConnection():
    
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    
    session['username'] = 'New user'
    print('connected')
    
    
    try:
        print "before query in connect"
        query =cur.mogrify("SELECT c.message, s.sender FROM chat AS c CROSS JOIN usersChat AS s WHERE c.chat_id = s.chat_id")
        print "after query"
        cur.execute(query)
        print query
        
        messages = cur.fetchall()
        print messages
        
        for message in messages:
            tmp = {'text': message[1], 'name': message[0] }
            print(message)
            emit('message', tmp)
    
    except:
        print("Error in database")        

@socketio.on('message', namespace='/iss')
def new_message(message):
    
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    senderUser = session['username']

    try:
        print('message: ' + str(message))
        print('senderUser: ' + str(senderUser))
        userQuery = cur.mogrify("""INSERT INTO usersChat (sender) VALUES %s;""", (senderUser,))
        msgQuery = cur.mogrify("""INSERT INTO chat message VALUES  %s;""", (message,))
        cur.execute(msgQuery)
        print("message added to database")
        conn.commit()
        
        tmp = {'text': message, 'name': senderUser}
        emit('message', tmp, broadcast=True)
    except:
        print("Error inserting")
        conn.rollback()



print ("before app route")


#for displaying html pages        
@app.route('/')
def mainIndex():
    print 'in hello world'
    # not sure we need this, but might be helpful later on
    logged = 0
    if 'username' in session:
        logged = 1
    
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        profQuery = cur.mogrify("SELECT name, views from events UNION SELECT name, views from people ORDER BY views desc LIMIT 10;")
        cur.execute(profQuery)
        rows = cur.fetchall()
        print profQuery
    except:
        print("Error executing SELECT statement")    
    
    return render_template('index.html', SelectedMenu = 'Index', topten = rows)
    
    
@app.route('/index.html')
def dashIndex():
    print 'in hello world'
    
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        profQuery = cur.mogrify("SELECT name, views from events UNION SELECT name, views from people ORDER BY views desc LIMIT 10;")
        cur.execute(profQuery)
        rows = cur.fetchall()
        print profQuery
    except:
        print("Error executing SELECT statement") 
    
    return render_template('index.html', SelectedMenu = 'Index', topten = rows)

    
@app.route('/SuggestEvent.html', methods=['GET','POST'])
def suggestEvent():
    print 'in forms'

    if request.method == 'POST':
        eventName = request.form['eventName']
        eventLoc = request.form['eventLoc']
        email = request.form['senderEmail']
        # file upload request 
        # 2 options requests
        importance = request.form['importance']
        time = request.form['timePeriod']         
        eventDesc = request.form['eventDesc']
        


        receiver=['ratemyhistory@gmail.com']
        sender = ['ratemyhistory@gmail.com']
                
        message = "<p>Here is a suggested Event:<br /><br />"
        message += "<b>Event Name: </b>" + eventName + "<br />"
        message += "<b>Event Location: </b>" + eventLoc + "<br />"
        message += "<b>Importance: </b>" + importance + "<br />"
        message += "<b>Time: </b>" + time + "<br />"
        message += "<b>Description: </b>" + eventDesc + "<br />"
        message += "<b>User Email: </b>" + email + "<br />"
        print(message)
        message += "<br /><br />Thank you, <br />Rate My History User"
        
        msg = MIMEMultipart('alternative')
        emailMsg = MIMEText(message, 'html')
        msg.attach(emailMsg)
                
        msg['Subject'] = 'Suggest Event'
        msg['From'] = 'ratemyhistory@gmail.com'
        msg['To'] = 'ratemyhistory@gmail.com'
               
        try:
            smtpObj = smtplib.SMTP("smtp.gmail.com", 587)
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.login('ratemyhistory@gmail.com', 'zacharski350')
            smtpObj.sendmail(sender, receiver, msg.as_string())    
            smtpObj.quit()
            print "Successfully sent email"
            complete = True
        except Exception as e:
            print(e)

        
    return render_template('SuggestEvent.html', SelectedMenu = 'SuggestEvent')
    
@app.route('/SuggestPerson.html', methods=['GET','POST'])
def suggestPerson():
    print 'in forms'
    
    
    return render_template('SuggestPerson.html', SelectedMenu = 'SuggestPerson')

    
@app.route('/profile.html')
def profile():
    print 'in profile'
    if session['loggedIn'] == 'Yes':
        uEmail = session['email']
        print uEmail
        conn = connectToDB()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            profQuery = cur.mogrify("SELECT Firstname, Lastname, Address, Company, Job, Fax, Email, Phone FROM users WHERE Email = %s LIMIT 1;", (uEmail,))
            cur.execute(profQuery)
            print profQuery
        except:
	        print("Error executing SELECT statement")
        pageStuff = cur.fetchall()
        entry = pageStuff[0]
        print entry[1]
    
    else:
        print "Error: Not logged in"
        return render_template('index.html', SelectedMenu = 'Index')
    
    return render_template('anotherProfile.html', pageInfo=entry, SelectedMenu = 'Profile')  
    
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
        
        email = request.form['email']
       
        
        regQuery = cur.mogrify("SELECT Email FROM users WHERE Email = %s", (email,))
        print (regQuery)
        cur.execute(regQuery)
        
        rows=cur.fetchall()
        print ("rows")
        
        if (rows == []):
            check = request.form['password']
            check2 = request.form['pwConfirm']
            
            if (check == check2):
            
                #dont have all users table datatypes, but we can work on that later
                regAddQuery = cur.mogrify("""INSERT INTO users (Username, Email, Password, Firstname, Lastname, Company, Job, Address, City, Country, Phone, Fax)
                    VALUES(%s, %s, crypt(%s, gen_salt('bf')), %s, %s, %s, %s, %s, %s, %s, %s, %s);""", (request.form['userName'],request.form['email'],request.form['password'],
                    request.form['firstName'],request.form['lastName'],request.form['comp'],request.form['prof'],request.form['address'],request.form['city'],
                    request.form['country'],request.form['phoneNumber'],request.form['faxNumber']))
                print (regAddQuery)
                
                cur.execute(regAddQuery)
                print("after add execute")
                #commented commit until I know the query is printing right
                conn.commit()
                print("person registered")
            else:
                print("passwords dont match, cant register")
            
        else:
            print ("email is taken so user exists")
            
    return render_template('register.html', SelectedMenu = 'Register')
    
@app.route('/AddEvent.html', methods=['GET','POST'])
def addEvent():
    print 'in event addition'
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    
    
    
    
    if request.method == 'POST':
        print ("in requests")       
        # eventName = request.form['addEventName']
        # eventLoc = request.form['addEventLoc']
        # email = request.form['addSenderEmail']
        # # file upload request 
        # eventDesc = request.form['addEventDesc']
        # # 2 options requests
        # importance = request.form['addImportance']
        # date = request.form['year']
        print (request.form["addEventName"])
        print (request.form["addEventLoc"])
        print (request.form["addEventDesc"])
        print (request.form["year"])
        addEventQuery=cur.mogrify("""INSERT INTO events (Name, Location, Description, Year) Values(%s, %s, %s, %s);""", (request.form['addEventName'],request.form['addEventLoc'],request.form['addEventDesc'], request.form['year'],))
        print addEventQuery
        cur.execute(addEventQuery)
        conn.commit()
    
    
    
    return render_template('AddEvent.html', SelectedMenu = 'AddEvent')

@app.route('/AddPerson.html', methods=['GET','POST'])
def addPerson():
    print 'in forms'
    
    
    return render_template('AddPerson.html', SelectedMenu = 'AddPerson')
    
    
@app.route('/timeline.html')
def timeline():
    print 'in timeline'
    
    return render_template('timeline.html', SelectedMenu = 'Timeline')
    
    
@app.route('/search.html')
def search():
    print 'in search'
    
    return render_template('search.html', SelectedMenu = 'searchengine')
 
 
@socketio.on('identify', namespace='/iss')
def on_identify(message):
    pass
 
    
@socketio.on('userLogin', namespace='/iss')
def on_login(data):
    print "in logincheck"
    pw = data['password']
    userEmail = data['email']
    
    #print (user)
    print (userEmail)
    print 'login '  + pw
    #session['logged'] = 0
    
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    print('connected')
    
    userQuery = cur.mogrify("select email from users where email = %s", (userEmail,))
    cur.execute(userQuery)
    userResult = cur.fetchone()
    
    if userResult:
        print 'already there'
        loginQuery = cur.mogrify("select Username, Email from users WHERE Email = %s AND Password = crypt(%s, Password)" , (userEmail, pw,))
        cur.execute(loginQuery) 
        print ('query executed')
    
        result = cur.fetchone()
        if result:
            print('logged in!')
            print('saving information to the session...')
            #needs work to pass to javascript to limit the message send function
            #session['logged'] = json.dumps('true')
            session['logged'] = 1
            session['username'] = result['username']
            emit('logged', {'logged_in' : session['logged'] })
            return redirect(url_for('mainIndex'))
        else:
            print ('incorrect login information')
            session['logged'] = 0
            emit ('logged',{'logged_in' : session['logged'] })
            return redirect(url_for('login'))

# def loggedIn(logged):
#     log = logged
#     return log          
    #updateRoster()
@socketio.on('logout', namespace='/iss')
def on_disconnect(data):
    print("i am here")
    session['logged'] = 0
    emit('logged', {'logged_in' : session['logged']})
    print 'user disconnected'




@app.route('/login.html')
def login():
    print 'in login'
    # conn = connectToDB()
    # cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    # if request.method == 'POST':
    #     print "HI"
    #     email = request.form['email']
    #     password = request.form['password']

    #     loginQuery = cur.mogrify("select Username, Email from users WHERE Email = %s AND Password = crypt(%s, Password)" , (email, password,))
    #     cur.execute(loginQuery)
    #     print loginQuery
    #     result = cur.fetchall()
    #     fullResult = result[0]


    #     print('logged in')
    #     print('name = ', fullResult['username'])
    #     session['userName'] = fullResult['username']
    #     session['loggedIn'] = 'Yes'
    #     session['email'] = fullResult['email']
    #     print session['userName']
            
    #     return redirect(url_for('mainIndex'))
            
    
        
    return render_template('login.html', SelectedMenu = 'Login')
    
    
@app.route('/logout')
def logout():
    print('removing session variables')
    del session['userName']
    session['loggedIn'] = 'No'
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
        socketio.run(app, host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)