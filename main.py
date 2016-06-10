# Python 2.x wordt hier gebruikt(meer bepaald 2.7)
# Aangezien flask-mysqldb een bitch is om te installeren in Python 3.5
# :)
from flask import Flask, request, render_template, jsonify, make_response, session, abort, redirect, send_file, json
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

# Wil je debuggen? gebruik app.logger.warning("boodschap")

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
    cur.execute(''' SELECT STU_id, STU_voornaam, STU_achternaam FROM student WHERE STU_mail = '%s' AND STU_paswoord = '%s' ''' % (mail, paswoord))
    rv = cur.fetchone()
    if str(rv) != '()':
        session['student_logged_in'] = True
        session['student_id'] = str(rv[0]).strip('(),')
        session['student_voornaam'] = str(rv[1]).strip('(),')
        app.logger.warning(session.get('student_voornaam'))
        session['student_achternaam'] = str(rv[2]).strip('(),')
        # studentnaam = str(rv[1]).strip('(),') + " " + str(rv[2]).strip('(),')
        return "1"
    else:
        session['student_logged_in'] = False
        return "0"

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
        naam = session.get('student_voornaam') + " " + session.get('student_achternaam')
        return render_template('student/dashboard.html', naam=naam)
    else:
        return render_template('error405.html')

## Slaag de rol op voor de belbin test van de student

@app.route('/roltoevoegen', methods=['POST'])
def roltoevoegen():
    rol = request.form['rol'];
    cur = mysql.connection.cursor()
    studentid = str(session.get('student_id'))
    cur.execute(''' UPDATE student SET STU_rol = '{0}' where STU_id = '{1}' '''.format(rol, studentid))
    mysql.connection.commit()
    return "1"


## JSON voor de quiz meegeven
@app.route('/belbintestjson')
def belbintestjson():
    return send_file("static/belbintest.json")


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
    school = request.form['school'];

    cur = mysql.connection.cursor()
    cur.execute(" INSERT INTO student (STU_voornaam, STU_achternaam, STU_mail, STU_paswoord, STU_school) VALUES ('%s', '%s', '%s', '%s', '%s') " % (voornaam, achternaam, mail, paswoord, school))
    mysql.connection.commit() # Is nodig voor inserts en updates, wat da wel vrij logisch klinkt als je het gevonden hebt, maar hoyl f*ck duurt het lang om dees te vinden
    return "done"


## Laat docent info van de student zien
@app.route('/studentenbekijken', methods=['GET', 'POST'])
def studentenbekijken():
    cur = mysql.connection.cursor()
    cur.execute(''' SELECT STU_id, STU_voornaam, STU_achternaam, STU_school, STU_rol FROM student ''')
    rows = [x for x in cur]
    cols = [x[0] for x in cur.description]
    studenten = []
    for row in rows:
        student = {}
        for prop, val in zip(cols, row):
            student[prop] = val
        studenten.append(student)
    studentenJSON = json.dumps(studenten)
    return studentenJSON


@app.route('/studentengroepenopvragen', methods=['GET'])
def studentengroepenopvragen():
    cur = mysql.connection.cursor()
    cur.execute(''' SELECT g.GRO_naam, s.STU_voornaam, s.STU_achternaam, s.STU_rol, s.STU_id  FROM groep g INNER JOIN student s on g.GRO_lidnaam = s.STU_id ''')
    rows = [x for x in cur]
    cols = [x[0] for x in cur.description]
    groepen = []
    for row in rows:
        groep = {}
        for prop, val in zip(cols, row):
            groep[prop] = val
        groepen.append(groep)
    groepenJSON = json.dumps(groepen)
    return groepenJSON

@app.route('/studentaangroeptoevoegen', methods=['POST'])
def studentaangroeptoevoegen():
    groepsnaam = request.form['groep'];
    studentid = request.form['studentid'];
    cur = mysql.connection.cursor()
    cur.execute(" INSERT INTO groep (GRO_naam, GRO_lidnaam) VALUES ('%s', '%s') " % (groepsnaam, studentid))
    mysql.connection.commit() # Is nodig voor inserts en updates, wat da wel vrij logisch klinkt als je het gevonden hebt, maar hoyl f*ck duurt het lang om dees te vinden
    return "done"
############################# VARIA
## Als een gebruiker naar een andere plaats gaat

@app.errorhandler(404)
def paginanietgevonden(e):
    return render_template('error404.html', e=e)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
