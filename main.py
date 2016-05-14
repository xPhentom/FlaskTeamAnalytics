from flask import Flask, request, render_template, json
from flask.ext.mysqldb import MySQL
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)

# MySQL config
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'DoNoH4rmLeaveNoTr4cks'
app.config['MYSQL_DB'] = 'teamanalytics'
app.config['MYSQL_HOST'] = '104.131.116.53'
mysql = MySQL(app)

@app.route('/')
def index():
    #cur = mysql.connection.cursor()
    return render_template("index.html")
    conn = mysql.connect()
    cursor = conn.cursor()

if __name__ == '__main__':
    app.run(port=5000, debug=True)
