from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    class_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    lecture_1 = db.Column(db.String(10), nullable=False)
    lecture_2 = db.Column(db.String(10), nullable=False)
    lecture_3 = db.Column(db.String(10), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        surname = request.form['surname']
        first_name = request.form['first_name']
        class_name = request.form['class_name']
        email = request.form['email']
        lecture_1 = request.form['lecture_1']
        lecture_2 = request.form['lecture_2']
        lecture_3 = request.form['lecture_3']
        
        new_student = Student(surname=surname, first_name=first_name,
                              class_name=class_name, email=email,
                              lecture_1=lecture_1, lecture_2=lecture_2,
                              lecture_3=lecture_3)
        db.session.add(new_student)
        db.session.commit()
        
        flash('Registration successful!', 'success')
        return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/admin', methods=['GET'])
def admin():
    students = Student.query.all()
    return render_template('admin.html', students=students)

@app.cli.command('init-db')
def init_db():
    """Initialize the database."""
    db.create_all()
    print('Initialized the database.')

if __name__ == '__main__':
    app.run(debug=True)
