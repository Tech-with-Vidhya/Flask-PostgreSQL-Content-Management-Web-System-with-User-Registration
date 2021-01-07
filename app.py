from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
#from flask_sqlalchemy import *
#from config import host, port, database, user, password
#from flask_migrate import Migrate

app = Flask(__name__)


ENV = 'Dev'

if ENV == 'Dev':
    app.debug = True
    #app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    #app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:vidhya123$@localhost:5432/postgres"
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:vidhya123$@localhost/postgres"
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
#migrate = Migrate(app, db)


class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email_address = db.Column(db.String(50), nullable=False, unique=True)
    gender_u = db.Column(db.String(50), nullable=False)
    languages_u = db.Column(db.String(50), nullable=False)

    def __init__(self, first_name, last_name, email_address, gender_u, languages_u):
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.gender_u = gender_u
        self.languages_u = languages_u

    def __repr__(self):
        return f"<User {self.first_name}>"

class Articles(db.Model):
    __tablename__ = 'articles'
    article_id = db.Column(db.Integer, primary_key=True)
    article_name = db.Column(db.String(500), nullable=False)
    article_description = db.Column(db.String(50000), nullable=False)

    def __init__(self, article_name, article_description):
        self.article_name = article_name
        self.article_description = article_description

    def __repr__(self):
        return f"<Article {self.article_name}>"

@app.route('/')
def home():
    # Syntax 1 to query the database table named "Articles"
    #p_result = Articles.query.all()
    # Syntax 2 to query the database table named "Articles"
    p_result = db.session.query(Articles).all()
    return render_template('home.html', result=p_result)

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/success', methods = ["POST"])
def success():
    global p_firstname, p_lastname, p_email, p_gender, p_languages
    p_firstname = request.form["firstname"]
    p_lastname = request.form["lastname"]
    p_email = request.form["email"]
    p_gender = request.form["gender"]
    p_languages = request.form["languages"]
    #return "User Registration Successful" + "\n" + "First Name: " + p_firstname + "\n" + "Last Name: " + p_lastname + "\n" + "Email Address: " + p_email + "\n" + "Gender: " + p_gender + "\n" + "Languages: " + p_languages

    if p_firstname == '' or p_lastname == '' or p_email == '':
        return render_template('register.html', message_1='Please enter inputs for all the available fields.')
    elif p_firstname == '' and p_lastname == '' and p_email == '':
        return render_template('register.html', message_1='Please enter inputs for all the available fields.')
    else:
        user = Users(p_firstname, p_lastname, p_email, p_gender, p_languages)
        db.session.add(user)
        db.session.commit()
        return render_template('register.html', message_4='New user is created successfully...')


@app.route('/userdetails')
def userdetails():
    #p_userdata = db.session.query(Users).filter(lower(Users.email_address)==lower(p_email).get()
    #p_userdata = db.session.query(Users).filter(Users.email_address == p_email)
    #p_userdata = db.session.query(Users).filter(Users.email_address == 'test1@test.com')
    #success()
    '''
    db.session.query(Users).all()
        if db.session.query(Users).filter(Users.email_address == success.p_email) == True:
            p_userdata = Users(first_name, last_name, email_address, gender_u, languages_u)
            return render_template('userdetails.html', userdata=p_userdata)
            #return render_template('userdetails.html')
    '''

    p_userdata = db.session.query(Users).filter(Users.email_address == p_email)
    return render_template('userdetails.html', userdata=p_userdata)

@app.route('/articles')
def articles():
    return render_template('articles.html')

@app.route('/process', methods = ["POST"])
def process():
    p_articlename = request.form["articlename"]
    p_articledescription = request.form["articledescription"]
    #return p_articlename + " " + p_articledescription

    if p_articlename == '' or p_articledescription == '':
        return render_template('articles.html', message_2='Please enter inputs for all the available fields.')
    elif p_articlename == '' and p_articledescription == '':
        return render_template('articles.html', message_2='Please enter inputs for all the available fields.')
    else:
        # Instance or Object of type class named "Articles"
        #article = Articles(article_name=p_articlename, article_description=p_articledescription)
        # article = Articles(article_name, article_description)
        # article = Articles(p_article_name, p_article_description)
        # article = Articles(articlename, articledescription)
        article = Articles(p_articlename, p_articledescription)
        db.session.add(article)
        db.session.commit()
        #p_result = db.session.query(Articles).all()
        return render_template('articles.html', message_3='Article created successfully...')


@app.route('/references')
def references():
    return render_template('references.html')

if __name__ == "__main":
    app.run()