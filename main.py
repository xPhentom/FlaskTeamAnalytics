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

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST': #Wat als we een post krijgen
        mail = request.form['mail'];
        paswoord = request.form['paswoord'];
        cur = mysql.connection.cursor()
        cur.execute(''' SELECT STU_voornaam FROM student WHERE STU_mail = '%s' AND STU_paswoord = '%s' ''' % (mail, paswoord))
        rv = cur.fetchall()
        if str(rv) != '()':
            session['logged_in'] = True
            return "1"
        else:
            session['logged_in'] = False
            return "0"
    else: # Als het geen post is, zal het een request zijn
        return render_template('index.html')


@app.route('/student/dashboard.html', methods=['GET', 'POST'])
def docentdashboard():

    if session.get('logged_in') == True:
        return render_template('student/dashboard.html')
    else:
        return render_template('error404.html')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
