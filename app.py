#!/usr/bin/python3
import os
from flask import Flask, render_template, request, redirect,url_for,redirect,session
from flask_mail import Mail, Message
from form_contact import ContactForm, csrf
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect,form
#from flask import Flask, url_for, render_template, request, redirect, session
mail = Mail()
csrf = CSRFProtect()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
db.create_all()

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
csrf.init_app(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'tahseen.khan1009@gmail.com'
app.config['MAIL_PASSWORD'] = 'chaman123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'tahseen.khan1009@gmail.com'
mail.init_app(app)

class User(db.Model):
    """ Create user table"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.route('/', methods=['GET', 'POST'])
def index():
    """ Session control"""
    if not session.get('logged_in'):
        return render_template('views/home/index.html')
    else:
        if request.method == 'POST':
            username = getname(request.form['username'])
            return render_template('views/home/index.html', data=getfollowedby(username))
        return render_template('views/home/index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login Form"""
    if request.method == 'GET':
        return render_template('views/login/login.html')
    else:
        name = request.form['username']
        passw = request.form['password']
        try:
            data = User.query.filter_by(username=name, password=passw).first()
            if data is not None:
                session['logged_in'] = True
                return redirect(url_for('views/home/index'))
            else:
                return 'Dont Login'
        except:
            return "Dont Login"

@app.route('/register/', methods=['GET', 'POST'])
def register():
    """Register Form"""
    if request.method == 'POST':
        #csrf.generate_csrf()
        new_user = User(
            username=request.form['username'],
            password=request.form['password'])
        db.session.add(new_user)
        db.session.commit()
        return render_template('views/login/login.html',form=form)
    return render_template('views/register/register.html',form=form)

@app.route("/logout")
def logout():
    """Logout Form"""
    session['logged_in'] = False
    return redirect(url_for('index'))


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        print('-------------------------')
        print(request.form['name'])
        print(request.form['email'])
        print(request.form['subject'])
        print(request.form['message'])
        print('-------------------------')
        send_message(request.form)
        return redirect('/success')

    return render_template('views/contacts/contact.html', form=form)

@app.route('/success')
def success():
    return render_template('views/home/index.html')

def send_message(message):
    print(message.get('name'))
    recipient=message.get('email')
    msg = Message(message.get('subject'),
            #sender = ['tahseen.khan1009@gmail.com'],
            recipients = [recipient],

            body= message.get('message')
    )
    mail.send(msg)

if __name__ == "__main__":
    #app.run(debug = True)
    app.debug = True
    app.secret_key = "123"
    db.create_all()
    #sys.setrecursionlimit(limit)
    csrf.init_app(app)
    app.run(host='0.0.0.0')
