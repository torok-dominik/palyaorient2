from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///registrations.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    lecture1 = db.Column(db.String(10), nullable=False)
    lecture2 = db.Column(db.String(10), nullable=False)
    lecture3 = db.Column(db.String(10), nullable=False)

db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/student_registration', methods=['GET', 'POST'])
def student_registration():
    if request.method == 'POST':
        email = request.form['email']
        lecture1 = request.form['lecture1']
        lecture2 = request.form['lecture2']
        lecture3 = request.form['lecture3']
        
        student = Student(email=email, lecture1=lecture1, lecture2=lecture2, lecture3=lecture3)
        try:
            db.session.add(student)
            db.session.commit()
            return redirect(url_for('index'))
        except IntegrityError:
            db.session.rollback()
            return "E-mail már használatban van!"

    return render_template('student_registration.html')

@app.route('/admin_login')
def admin_login():
    return render_template('admin_login.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    students = Student.query.all()
    return render_template('admin_dashboard.html', students=students)

if __name__ == '__main__':
    app.run(debug=True)
