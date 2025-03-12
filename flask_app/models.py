from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class Teilnehmer(db.Model):
    __tablename__ = 'TEILNEHMER'
    id_num = db.Column(db.Integer, primary_key=True)
    vorname = db.Column(db.String(50), nullable=False)
    nachname = db.Column(db.String(50), nullable=False)
    pw = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.pw = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw, password)
    
class Seminar(db.Model):
    __tablename__ = 'SEMINAR'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    street = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    time = db.Column(db.String(5), nullable=False)


class Buchung(db.Model):
    __tablename__ = 'BUCHUNG'
    id = db.Column(db.Integer, primary_key=True)
    teilnehmer_id = db.Column(db.Integer, db.ForeignKey('TEILNEHMER.id_num'), nullable=False)
    seminar_id = db.Column(db.Integer, db.ForeignKey('SEMINAR.id'), nullable=False)
    seminar = db.relationship('Seminar', backref='buchungen')
