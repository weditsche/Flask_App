from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .models import Teilnehmer, Seminar, Buchung
from . import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('main.home'))
    return redirect(url_for('main.login'))

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        id_num = request.form.get('id_num')
        pw = request.form.get('pw')
        user = Teilnehmer.query.filter_by(id_num=id_num).first()
        if user and user.check_password(pw):
            session['user_id'] = user.id_num
            flash('Logged in successfully.')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid ID or password.')
    return render_template('login.html')

@main_bp.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    return render_template('home.html')

@main_bp.route('/seminars')
def seminars():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    seminars = Seminar.query.all()
    return render_template('seminars.html', seminars=seminars)

@main_bp.route('/book/<int:seminar_id>')
def book(seminar_id):
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    booking = Buchung(teilnehmer_id=session['user_id'], seminar_id=seminar_id)
    db.session.add(booking)
    db.session.commit()
    flash('Seminar booked successfully.')
    return redirect(url_for('main.seminars'))

@main_bp.route('/mybookings')
def mybookings():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    bookings = Buchung.query.filter_by(teilnehmer_id=session['user_id']).all()
    return render_template('mybookings.html', bookings=bookings)

@main_bp.route('/cancel/<int:booking_id>')
def cancel(booking_id):
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    booking = Buchung.query.filter_by(id=booking_id, teilnehmer_id=session['user_id']).first()
    if booking:
        db.session.delete(booking)
        db.session.commit()
        flash('Booking cancelled successfully.')
    else:
        flash('Booking not found or not authorized.')
    return redirect(url_for('main.mybookings'))

@main_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully.')
    return redirect(url_for('main.login'))

