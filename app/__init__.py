from flask import Flask
from flask_mail import Mail

import pymysql

pymysql.install_as_MySQLdb()

def create_app():
    app = Flask(__name__)


    # Configurarea aplicației pentru Flask-Mail
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Serverul SMTP
    app.config['MAIL_PORT'] = 587                # Portul pentru TLS
    app.config['MAIL_USE_TLS'] = True            # Utilizarea TLS
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = 'mihaihodis98@gmail.com'  # Adresa ta de Gmail
    app.config['MAIL_PASSWORD'] = 'vvhqmluvctgyvmig'  # Parola pentru Gmail (poate fi o parolă pentru aplicație)

    # Inițializarea Flask-Mail
    mail = Mail(app)

    # Configurarea bazei de date
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'brendaUser'
    app.config['MYSQL_PASSWORD'] = '1234'
    app.config['MYSQL_DB'] = 'brendaDB'

    # Setarea cheii secrete pentru a utiliza flsh
    app.config['SECRET_KEY'] = '1234'

    # Funcție pentru conectarea la baza de date
    def get_db_connection():
        try:
            connection = pymysql.connect(
                host=app.config['MYSQL_HOST'],
                user=app.config['MYSQL_USER'],
                passwd=app.config['MYSQL_PASSWORD'],
                db=app.config['MYSQL_DB']
            )
            return connection
        except pymysql.MySQLError as e:
            print(f"Error: {e}")
            return None

    # Expunem funcția `get_db_connection` pentru a fi folosită în alte module
    app.get_db_connection = get_db_connection
    app.mail = mail # Expunem si mail pentru a fi folosit in routes

    # Importăm rutele după ce am creat aplicația pentru a evita circular import
    with app.app_context():
        from . import routes

    return app
