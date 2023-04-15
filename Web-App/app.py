from flask import redirect,Flask, request, render_template, session
from argon2 import PasswordHasher
import sqlite3
phash = PasswordHasher()
app = Flask(__name__)

secretkey = open('KEY.txt','r')
app.secret_key = secretkey.read()

@app.route("/")
def test():
    return redirect('/login')


@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == None or password == None or username == '' or password == '':
            error = "Empty password or username"
            return render_template('error.html', error=error)
        username = str(username)
        password = str(password)
        if any(k in ('"', "'", "(", ")", "{", "}", "[", "]",";",":"," ") for k in username):
            error = "Username contains illegal characters"
            return render_template('error.html',error = error)
        else:
            connection = sqlite3.connect("../users.db")
            check = connection.execute('''SELECT * FROM usernames WHERE username='{}' LIMIT 1 '''.format(username))
            print('''SELECT * FROM usernames WHERE username='{}' LIMIT 1 '''.format(username))
            check2=()
            for row in check:
                check2 = row
                break
            connection.commit()
            print(check2)
            if check2!=():
                try:
                    if check2[0] == username and phash.verify(check2[1],password):
                        session['username'] = username
                        return redirect('/account')
                except:
                    error = "Username or password are incorrect"
                    return render_template('error.html',error = error)
            else:
                error = "Username not found"
                return render_template('error.html', error=error)
        error = "Something went wrong"
        return render_template('error.html',error = error)
    else:
        if 'username' in session.keys():
            if session['username']==None:
                return render_template("login.html")
            else:
                return redirect('/account')
        else:
            session['username'] = None
            return render_template("login.html")

@app.route("/register",methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == None or password == None:
            error = "Empty password or username"
            return render_template('error.html',error = error)
        else:
            username = str(username)
            password = str(password)
            if any(k in ('"', "'", "(", ")", "{", "}", "[", "]",";",":") for k in username):
                error="Username contains illegal characters"
                return render_template('error.html',error = error)
            connection = sqlite3.connect("../users.db")
            check = connection.execute('''SELECT * FROM usernames WHERE username='{}' LIMIT 1 '''.format(username))
            check2 = ()
            for row in check:
                check2 = row
                break
            connection.commit()
            print(check2)
            if check2 == ():
                a = sqlite3.connect('../users.db')
                a.execute("""INSERT INTO usernames(username,password) 
                VALUES('{}','{}')""".format(username,phash.hash(password)))
                a.commit()
                session['username']=username
                return redirect('/account')
            else:
                error = "Account with this nickname already exists"
                return render_template('error.html',error = error)
    else:
        return render_template("register.html")
@app.route('/account')
def account():
    if 'username' in session.keys():
        if session['username']==None:
            return redirect('login')
        else:
            return render_template('account.html')
    else:
        return redirect('/login')
@app.route('/logout')
def logout():
    session['username']=None
    return redirect('/login')
app.run()