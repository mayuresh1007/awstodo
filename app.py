from flask import Flask,render_template,request,redirect,session,url_for
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

app = Flask(__name__)
app.secret_key = "imaxxmaki" # used for session module keep it secrete

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
def index():
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