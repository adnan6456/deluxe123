from flask import Flask,request,redirect
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import pymysql
from flask_mail import Mail
from flask_mail import Message
from flask_login import LoginManager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional
import email_validator

pymysql.install_as_MySQLdb()
engine = create_engine('mysql://root:root@127.0.0.1:3306/test?charset=utf8')


local_server = True    
app = Flask(__name__)
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'apnakhan6456@gmail.com',
    MAIL_PASSWORD = '64563371'
    )
mail = Mail(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/deluxe'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
import os
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

pymysql.install_as_MySQLdb()

class Contacts(db.Model):
    name = db.Column(db.String(50), unique=False, primary_key=True, nullable=False)
    message = db.Column(db.String(160), unique=False, nullable=False)
    number = db.Column(db.String(12), unique=False, nullable=False)

class Users(db.Model):
    name = db.Column(db.String(120), unique=False, primary_key=True, nullable=False)
    email = db.Column(db.String(60), unique=False, nullable=False)
    number = db.Column(db.String(12), unique=False, nullable=False)
    password = db.Column(db.String(12), unique=False, nullable=False)
    center_name = db.Column(db.String(120), unique=False, nullable=False)
    center_add = db.Column(db.String(160), unique=False, nullable=False)


class User(db.Model):
    user = db.Column(db.String(120), unique=False, primary_key=True, nullable=False)
    password = db.Column(db.String(60), unique=False, nullable=False)

@login_manager.user_loader
def user_loader(user):
    return User.get(user)






    

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/store')
def store():
    return render_template("store.html")


@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")



@app.route('/contact', methods = ['GET', 'POST'])
def contact():
    if (request.method == "POST"):
        name = request.form.get('name')
        message = request.form.get('message')
        number = request.form.get('number')
        entry = Contacts(name = name, message = message, number = number)
        db.session.add(entry)
        db.session.commit()
       #''' mail.send_message('New Message From user ',
             #          sender='apnakhan6456@gmail.com',
                    #   recipients = 'adnankhan6456@gmail.com',
                     #  body = message
                   #    ) '''
        msg = Message('New Message From ' + name,
                      sender = 'apnakhan6456@gmail.com',
                      recipients = ['apnakhan6456@gmail.com'])
        msg.body = message +  " My Contact " + number
        mail.send(msg)
        return redirect('/')
    return render_template("contact.html")

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if (request.method == "POST"):
        name = request.form.get('name')
        email = request.form.get('email')
        number = request.form.get('number')
        password = request.form.get('password')
        center_name = request.form.get('center')
        center_add = request.form.get('center_add')
        entry = Users(name = name, email = email, number = number, password = password, center_name = center_name, center_add = center_add)
        db.session.add(entry)
        db.session.commit()
        msg = Message('User Registration Succesfull ' + name,
                      sender = 'apnakhan6456@gmail.com',
                      recipients = [email])
        msg.body = "Username :  " + email + " " + "Password : " + password
        mail.send(msg)
        return redirect('/login')

    return render_template("signup.html")

auth_bp = Blueprint(
    'auth_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

    
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if (request.method == 'POST'):
        currentuser = request.form.get('Username')
        currentpass = request.form.get('Password')
        entry = User(user = currentuser, password = currentpass)
        db.session.add(entry)
        db.session.commit()
    # Validate login attempt
    def validate():
        if currentuser == Users.query.filter_by(email=currentuser).first() and currentpass == Users.query.filter_by(password=currentpass).first() :
            return redirect('dashboard')
        else:
            return redirect('/')
    return render_template("login.html")



app.run(debug=True)








