# Python 2.x wordt hier gebruikt(meer bepaald 2.7)
# Aangezien flask-mysqldb een bitch is om te installeren in Python 3.5
# :)
from flask import Flask, request, render_template, jsonify, make_response, session, abort, redirect, send_file
# Flask is het framework die we gaan gebruiken
# Request is om de formvalues op te halen
# render_template is om html-pagina's boven te halen
# json is om vele data van een SQL-query te laten omvormen naar json
# Make_response
# Session is om sessions bij te houden zoals in php
# abort is om errors te gooien
from flask.ext.mysqldb import MySQL
# MySQL om met de MySQL database te spreken, komt vanuit de module flask-mysqldb
# from flask.ext.login import current_user ###### Zet dit terug als er een fout komt
# from flask.ext.session import Session ###### Zet dit terug als er een fout komt

app = Flask(__name__)

app.secret_key = "This is a secret key"

# Setup MySQL
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'DoNoH4rmLeaveNoTr4cks'
app.config['MYSQL_DB'] = 'teamanalytics'
app.config['MYSQL_HOST'] = '104.131.116.53'

mysql = MySQL(app)

## Homescreen

@app.route('/')
def index():
        return render_template('index.html')

################ Student login

@app.route('/inlogstudent', methods=['POST'])
def loginStudent():

    mail = request.form['mail'];
    paswoord = request.form['paswoord'];
    cur = mysql.connection.cursor()
    cur.execute(''' SELECT STU_id FROM student WHERE STU_mail = '%s' AND STU_paswoord = '%s' ''' % (mail, paswoord))
    rv = cur.fetchone()
    if str(rv) != '()':
        session['student_logged_in'] = True
        session['student_id'] = str(rv[0]).strip('(),') #id krijgt rare tekens
        return "1"
    else:
        session['student_logged_in'] = False
        return "0"

## JSON voor de quiz meegeven
@app.route('/belbintestjson')
def belbintestjson():
    return send_file("static/belbintest.json")

## Student rol opslaan

@app.route('/roltoevoegen', methods=['POST'])
def roltoevoegen():
    rol = request.form['rol'];
    cur = mysql.connection.cursor()
    studentid = str(session.get('student_id'))
    cur.execute(''' UPDATE student SET STU_rol = '{0}' where STU_id = '{1}' '''.format(rol, studentid))
    mysql.connection.commit()
    return "1"


################ Docent login

@app.route('/inlogdocent', methods=['POST'])
def loginDocent():

    mail = request.form['mail'];
    paswoord = request.form['paswoord'];
    cur = mysql.connection.cursor()
    cur.execute(''' SELECT DOC_id FROM docent WHERE DOC_mail = '%s' AND DOC_paswoord = '%s' ''' % (mail, paswoord))
    rv = cur.fetchone()
    if str(rv) != '()':
        session['docent_logged_in'] = True
        return "1"
    else:
        session['docent_logged_in'] = False
        return "0"

################### Alle andere spullen buiten het inloggen van de gebruikers
################### Beginnent met de student en daarna alles voor de docent
################### Als laatste komt alles wat nodig is om de site te draaien zonder specifiek te kijken naar student of docent


############################ STUDENT
## Check of student ingelogd is

@app.route('/student/dashboard.html', methods=['GET', 'POST'])
def studentdashboard():
    if session.get('student_logged_in') == True:
        return render_template('student/dashboard.html')
    else:
        return render_template('error405.html')

## Slaag de rol op voor de belbin test van de student

############################ DOCENT
## Check of docent ingelogd is

@app.route('/docent/dashboard.html', methods=['GET', 'POST'])
def docentdashboard():
    if session.get('docent_logged_in') == True:
        return render_template('docent/dashboard.html')
    else:
        abort(403)

## Laat docent student toevoegen
@app.route('/studenttoevoegen', methods=['GET', 'POST'])
def studenttoevoegen():
    voornaam = request.form['voornaam'];
    achternaam = request.form['achternaam'];
    paswoord = request.form['paswoord'];
    mail = request.form['mail'];
    klas = request.form['klas'];
    les = request.form['les'];

    cur = mysql.connection.cursor()
    cur.execute(" INSERT INTO student (STU_voornaam, STU_achternaam, STU_mail, STU_paswoord, STU_klas, STU_les) VALUES ('%s', '%s', '%s', '%s', '%s', '%s') " % (voornaam, achternaam, paswoord, mail, klas, les))
    mysql.connection.commit() # Is nodig voor inserts en updates, wat da wel vrij logisch klinkt als je het gevonden hebt, maar hoyl f*ck duurt het lang om dees te vinden
    return "done"


## Laat docent info van de student zien
@app.route('/studentenbekijken', methods=['GET', 'POST']) # Klinkt vrij tot zeer pedo
def studentenbekijken():
    cur = mysql.connection.cursor()
    cur.execute(''' SELECT STU_voornaam, STU_achternaam, STU_klas, STU_mail, STU_rol FROM student ''')
    return jsonify(data=cur.fetchall())

############################# VARIA
## Als een gebruiker naar een andere plaats gaat

@app.errorhandler(404)
def paginanietgevonden(e):
    return render_template('error404.html', e=e)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
