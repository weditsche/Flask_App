from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'  # SQLite database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'dev'  # For session management; change for production

db = SQLAlchemy(app)

# Database Models
class Teilnehmer(db.Model):
    __tablename__ = 'TEILNEHMER'
    id_num = db.Column(db.Integer, primary_key=True)
    vorname = db.Column(db.String(50), nullable=False)
    nachname = db.Column(db.String(50), nullable=False)
    pw = db.Column(db.String(128), nullable=False)

class Seminar(db.Model):
    __tablename__ = 'SEMINAR'
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(10), nullable=False)  # e.g. "YYYY-MM-DD"
    time = db.Column(db.String(5), nullable=False)    # e.g. "HH:MM"

class Buchung(db.Model):
    __tablename__ = 'BUCHUNG'
    id = db.Column(db.Integer, primary_key=True)
    teilnehmer_id = db.Column(db.Integer, db.ForeignKey('TEILNEHMER.id_num'), nullable=False)
    seminar_id = db.Column(db.Integer, db.ForeignKey('SEMINAR.id'), nullable=False)

# Create the tables before the first request (for demonstration purposes)
@app.before_first_request
def create_tables():
    db.create_all()

# Home route redirects to login if not logged in
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('seminars'))
    return redirect(url_for('login'))

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        id_num = request.form.get('id_num')
        pw = request.form.get('pw')
        user = Teilnehmer.query.filter_by(id_num=id_num, pw=pw).first()
        if user:
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

# Booking route: book a seminar
@app.route('/book/<int:seminar_id>')
def book(seminar_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    # Create a booking record
    booking = Buchung(teilnehmer_id=session['user_id'], seminar_id=seminar_id)
    db.session.add(booking)
    db.session.commit()
    flash('Seminar booked successfully.')
    return redirect(url_for('seminars'))

if __name__ == '__main__':
    app.run(debug=True)
