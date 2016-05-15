from flask import Flask, request, render_template, json, make_response, session
from flask.ext.mysqldb import MySQL
from flask.ext.login import current_user
from flask.ext.session import Session

app = Flask(__name__)

app.secret_key = "This is a secret key"

# Setup MySQL
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'DoNoH4rmLeaveNoTr4cks'
app.config['MYSQL_DB'] = 'teamanalytics'
app.config['MYSQL_HOST'] = '104.131.116.53'

mysql = MySQL(app)

################ Student login

@app.route('/')
def index():
        return render_template('index.html')


@app.route('/inlogstudent', methods=['POST'])
def loginStudent():

    mail = request.form['mail'];
    paswoord = request.form['paswoord'];
    cur = mysql.connection.cursor()
    cur.execute(''' SELECT STU_id FROM student WHERE STU_mail = '%s' AND STU_paswoord = '%s' ''' % (mail, paswoord))
    rv = cur.fetchall()
    if str(rv) != '()':
        session['student_logged_in'] = True
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
    rv = cur.fetchall()
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

############################ DOCENT
## Check of docent ingelogd is

@app.route('/docent/dashboard.html', methods=['GET', 'POST'])
def docentdashboard():
    if session.get('docent_logged_in') == True:
        return render_template('docent/dashboard.html')
    else:
        return render_template('error405.html')

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
    # , STU_achternaam, STU_mail, STU_paswoord, STU_klas, STU_les
    cur.execute(" INSERT INTO student (STU_voornaam, STU_achternaam, STU_mail, STU_paswoord, STU_klas, STU_les) VALUES ('%s', '%s', '%s', '%s', '%s', '%s') " % (voornaam, achternaam, paswoord, mail, klas, les))
    mysql.connection.commit()
    return "done"
############################# VARIA
## Als een gebruiker naar een andere plaats gaat

@app.errorhandler(404)
def paginanietgevonden(e):
    return render_template('error404.html', e=e)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
