from flask import Flask,render_template,request,redirect,session,url_for
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
import mysql.connector
import  os
from datetime import datetime

app = Flask(__name__)
app.secret_key=os.urandom(13) # for session purpose

conn=mysql.connector.connect(host="remotemysql.com",user="yk3kW2HtCF",password="4QmhiVOJx2",database="yk3kW2HtCF")
cursor=conn.cursor()



@app.route('/index',methods=['GET','POST'])
def index():
    if 'sno' in session:
        return render_template('index.html')
    else:
        return redirect('/')

@app.route('/',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if (username and email and password) == str(''):
            return ("please enter the values properly")

        else:
            cursor.execute("""INSERT INTO `Users`(`sno`,`username`,`email`,`password`) VALUES (NULL,'{}','{}','{}')""".format(username,email,password))
            conn.commit()
            return redirect('/index')

            cursor.execute("""SELECT * FROM `Users` WHERE `email` LIKE '{}'""".format(email))
            newuser = cursor.fetchall()
            session['email'] = newuser[0]
            return redirect('/index')

    return render_template('register.html')


@app.route('/login',methods=['GET','POST'])
def login():     
    if request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        cursor.execute("""SELECT * FROM `Users` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email,password))
        users = cursor.fetchall()
        # print(users)
        # print(users[0][1])

        if len(users)>0:
            session['sno']=users[0][0]
            session['username']=users[0][1]
            
            return redirect('/index')
        else:
            return render_template('register.html')
        return "hello"    
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('sno') or session.pop('username')
    return redirect('/')

# app.secret_key = "imaxxmaki" # used for session module keep it secrete

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    # date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_created = db.Column(db.DateTime, default=datetime.now)



@app.route('/',methods=['GET','POST'])
def uindex():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        imaxx =Todo(title=title,desc=desc)
        db.session.add(imaxx)
        db.session.commit()
    alltodo = Todo.query.all()
    return render_template('index.html',alltodo=alltodo)


@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title= request.form['title']
        desc= request.form['desc'] 
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title= title
        todo.desc= desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    alltodo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(alltodo)
    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)