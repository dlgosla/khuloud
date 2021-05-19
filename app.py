from flask import Flask, flash, url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
#from pymongo import MongoClient
from flask_restx import Resource, Api
from auth import Auth
import json


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

#client = MongoClient()
#db = client.dbname

#db = client["users"]

# test - id
#db.users.insert_one({'user_id' : 'test','user_pwd': 'test', 'user_name' : '정글','user_email': '.com','user_ordinal' : 1})

"""
api = Api(
    app,
    version='0.1',
    title="API Server",
    description="kloud api server",
    terms_url="/",
    license="MIT"
)

api.add_namespace(Auth, '/auth')
"""

class User(db.Model):
    """ Create user table"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, user_id, password):
        self.user_id = user_id
        self.password = password


@app.route('/', methods=['GET', 'POST'])
def home():
    """ Session control"""
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        if request.method == 'POST':
            return render_template('index.html')
        return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login Form"""
    if request.method == 'GET':
        return render_template('auth-sign-in.html')
    else:
        id = request.form['id']
        passw = request.form['password']
        try:
            data = User.query.filter_by(user_id=id, password=passw).first()
            if data is not None:
                session['logged_in'] = True
                return redirect(url_for('home'))
            else:
                return render_template("auth-sign-in.html", data = "아이디나 비밀번호가 일치하지 않습니다.")
        except:
            return render_template("auth-sign-in.html", data = "아이디나 비밀번호가 일치하지 않습니다.")

# 회원가입 
@app.route('/register/', methods=['GET', 'POST'])
def register():
    """Register Form"""
    
    if request.method == 'POST':
        id = request.form.get("id", type=str)
        password = request.form.get("password", type=str)
        re_password = request.form.get("password_confim", type=str)
         
        
        data = dict()

        if  User.query.filter_by(user_id=id).first() is not None:
            data = {"msg":"존재하는 id입니다."}

        elif id is "" or password is "" or re_password is "":
            data = {"msg":"입력되지 않은 항목이 있습니다."}

        elif password != re_password:
            data = {"msg": "비밀번호가 일치하지 않습니다."}

        elif request.form.get("customCheck1") == None:
            data = {"msg":"약관에 동의해주세요."}

        else:
            """
            user_info = {
                "id" : id,
                "password" : password
                }
            db.users.insert_one(user_info)
            """
            new_user = User(
                user_id=id,
                password=password)

            db.session.add(new_user)
            db.session.commit()

            return redirect("/login")

        return render_template("auth-sign-up.html", data = data)

    return render_template("auth-sign-up.html")


@app.route("/logout")
def logout():
    """Logout Form"""
    session['logged_in'] = False
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.debug = True
    db.create_all()
    app.secret_key = "123"
    app.run()