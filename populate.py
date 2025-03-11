import os
import csv
from my_flask_app import create_app, db
from my_flask_app.models import Teilnehmer, Seminar, Buchung

# Create the Flask app using your application factory.
app = create_app()

with app.app_context():
    # Ensure tables exist (this will create any missing tables)
    db.create_all()

    # Define sample data for participants and seminars.
    sample_users = [
        {"vorname": "Alice", "nachname": "Miller", "password": "password123"},
        {"vorname": "Bob", "nachname": "Smith", "password": "secret"}
    ]

    sample_seminars = [
        {"name": "Intro to Python", "street": "Main Street 1", "date": "2025-04-01", "time": "09:00"},
        {"name": "Advanced Flask", "street": "Second Avenue 20", "date": "2025-04-02", "time": "14:00"}
    ]

    # Populate the Teilnehmer table if it is empty.
    if Teilnehmer.query.count() == 0:
        for user in sample_users:
            t = Teilnehmer(vorname=user["vorname"], nachname=user["nachname"])
            t.set_password(user["password"])  # This stores the hashed password.
            db.session.add(t)
        db.session.commit()

    # Populate the Seminar table if it is empty.
    if Seminar.query.count() == 0:
        for sem in sample_seminars:
            s = Seminar(name=sem["name"], street=sem["street"], date=sem["date"], time=sem["time"])
            db.session.add(s)
        db.session.commit()

    # (The Buchung table is left empty by default.)

    # Create an "exports" folder to save CSV and text files.
    export_folder = "exports"
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)

    # Export the Teilnehmer table to CSV.
    teilnehmer_csv = os.path.join(export_folder, "teilnehmer.csv")
    with open(teilnehmer_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["id_num", "vorname", "nachname", "pw"])
        for t in Teilnehmer.query.all():
            writer.writerow([t.id_num, t.vorname, t.nachname, t.pw])

    # Export the Seminar table to CSV (including the new "name" column).
    seminar_csv = os.path.join(export_folder, "seminar.csv")
    with open(seminar_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "name", "street", "date", "time"])
        for s in Seminar.query.all():
            writer.writerow([s.id, s.name, s.street, s.date, s.time])

    # Export the Buchung table to CSV.
    buchung_csv = os.path.join(export_folder, "buchung.csv")
    with open(buchung_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "teilnehmer_id", "seminar_id"])
        for b in Buchung.query.all():
            writer.writerow([b.id, b.teilnehmer_id, b.seminar_id])

    # Create a text file listing the sample users with their plain-text passwords.
    users_txt = os.path.join(export_folder, "users_passwords.txt")
    with open(users_txt, mode='w', encoding='utf-8') as file:
        for user in sample_users:
            file.write(f"{user['vorname']} {user['nachname']}: {user['password']}\n")

    print("Database populated and data exported successfully.")
