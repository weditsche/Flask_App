from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# Use a SQLite database that will be created automatically in the project folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'dev'  # Change this for production

db = SQLAlchemy(app)

# Define models
class Teilnehmer(db.Model):
    __tablename__ = 'TEILNEHMER'
    id_num = db.Column(db.Integer, primary_key=True)
    vorname = db.Column(db.String(50), nullable=False)
    nachname = db.Column(db.String(50), nullable=False)
    pw = db.Column(db.String(128), nullable=False)  # Store a hashed password

    def set_password(self, password):
        self.pw = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw, password)

class Seminar(db.Model):
    __tablename__ = 'SEMINAR'
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(10), nullable=False)  # e.g., "YYYY-MM-DD"
    time = db.Column(db.String(5), nullable=False)   # e.g., "HH:MM"

class Buchung(db.Model):
    __tablename__ = 'BUCHUNG'
    id = db.Column(db.Integer, primary_key=True)
    teilnehmer_id = db.Column(db.Integer, db.ForeignKey('TEILNEHMER.id_num'), nullable=False)
    seminar_id = db.Column(db.Integer, db.ForeignKey('SEMINAR.id'), nullable=False)

# Home route: if logged in, show seminars; otherwise, go to login
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('seminars'))
    return redirect(url_for('login'))

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        id_num = request.form.get('id_num')
        pw = request.form.get('pw')
        user = Teilnehmer.query.filter_by(id_num=id_num).first()
        if user and user.check_password(pw):
            session['user_id'] = user.id_num
            flash('Logged in successfully.')
            return redirect(url_for('seminars'))
        else:
            flash('Invalid ID or password.')
    return render_template('login.html')

# List available seminars
@app.route('/seminars')
def seminars():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    seminars = Seminar.query.all()
    return render_template('seminars.html', seminars=seminars)

# Book a seminar
@app.route('/book/<int:seminar_id>')
def book(seminar_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    booking = Buchung(teilnehmer_id=session['user_id'], seminar_id=seminar_id)
    db.session.add(booking)
    db.session.commit()
    flash('Seminar booked successfully.')
    return redirect(url_for('seminars'))

# Optional: route to insert sample data if the tables are empty
@app.route('/initdata')
def initdata():
    if Teilnehmer.query.count() == 0:
        t1 = Teilnehmer(vorname='Alice', nachname='Miller')
        t1.set_password('password123')
        t2 = Teilnehmer(vorname='Bob', nachname='Smith')
        t2.set_password('secret')
        db.session.add_all([t1, t2])
        db.session.commit()
    if Seminar.query.count() == 0:
        s1 = Seminar(street='Main Street 1', date='2025-04-01', time='09:00')
        s2 = Seminar(street='Second Avenue 20', date='2025-04-02', time='14:00')
        db.session.add_all([s1, s2])
        db.session.commit()
    return "Sample data added."

if __name__ == '__main__':
    # Initialize the database immediately on startup
    with app.app_context():
        db.create_all()
    app.run(debug=True)
