from flask import Flask,render_template,request,redirect,session,url_for
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
import mysql.connector
import  os

app = Flask(__name__)
app.secret_key=os.urandom(13) # for session purpose

# conn=mysql.connector.connect(host="remotemysql.com",user="yk3kW2HtCF",password="4QmhiVOJx2",database="yk3kW2HtCF")
conn=mysql.connector.connect(host="myblogdatabase.clu8gz3nws6u.ap-south-1.rds.amazonaws.com",user="admin",password="mayuresh8855898076",database="sys")
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

            # cursor.execute("""SELECT * FROM `Users` WHERE `email` LIKE '{}'""".format(email))
            # newuser = cursor.fetchall()
            # session['email'] = newuser[0]
            # return redirect('/index')

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


if __name__ == "__main__":
    app.run(debug=True)