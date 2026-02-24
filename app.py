from flask import Flask, render_template, request, redirect, url_for
from models import db, Patient, Doctor, Appointment, Billing
from datetime import datetime
import os

app = Flask(__name__)

# ============================================================
# DATABASE CONFIGURATION (LOCAL + AZURE READY)
# ============================================================

database_url = os.environ.get("DATABASE_URL")

if database_url:
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://localhost/hospital_db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():
    return render_template("index.html")


# ============================================================
# PATIENT CRUD
# ============================================================

@app.route("/patients")
def view_patients():
    patients = Patient.query.all()
    return render_template("patients.html", patients=patients)


@app.route("/add_patient", methods=["POST"])
def add_patient():
    new_patient = Patient(
        name=request.form["name"],
        age=request.form["age"],
        gender=request.form["gender"],
        phone=request.form["phone"]
    )
    db.session.add(new_patient)
    db.session.commit()
    return redirect(url_for("view_patients"))


@app.route("/delete_patient/<int:id>")
def delete_patient(id):
    patient = Patient.query.get(id)
    db.session.delete(patient)
    db.session.commit()
    return redirect(url_for("view_patients"))


@app.route("/update_patient/<int:id>", methods=["GET", "POST"])
def update_patient(id):
    patient = Patient.query.get(id)

    if request.method == "POST":
        patient.name = request.form["name"]
        patient.age = request.form["age"]
        patient.gender = request.form["gender"]
        patient.phone = request.form["phone"]
        db.session.commit()
        return redirect(url_for("view_patients"))

    return render_template("update_patient.html", patient=patient)


# ============================================================
# DOCTOR CRUD
# ============================================================

@app.route("/doctors")
def view_doctors():
    doctors = Doctor.query.all()
    return render_template("doctors.html", doctors=doctors)


@app.route("/add_doctor", methods=["POST"])
def add_doctor():
    new_doctor = Doctor(
        name=request.form["name"],
        specialization=request.form["specialization"],
        phone=request.form["phone"]
    )
    db.session.add(new_doctor)
    db.session.commit()
    return redirect(url_for("view_doctors"))


@app.route("/delete_doctor/<int:id>")
def delete_doctor(id):
    doctor = Doctor.query.get(id)
    db.session.delete(doctor)
    db.session.commit()
    return redirect(url_for("view_doctors"))


@app.route("/update_doctor/<int:id>", methods=["GET", "POST"])
def update_doctor(id):
    doctor = Doctor.query.get(id)

    if request.method == "POST":
        doctor.name = request.form["name"]
        doctor.specialization = request.form["specialization"]
        doctor.phone = request.form["phone"]
        db.session.commit()
        return redirect(url_for("view_doctors"))

    return render_template("update_doctor.html", doctor=doctor)


# ============================================================
# APPOINTMENT CRUD
# ============================================================

@app.route("/appointments")
def view_appointments():
    appointments = Appointment.query.all()
    patients = Patient.query.all()
    doctors = Doctor.query.all()
    return render_template(
        "appointments.html",
        appointments=appointments,
        patients=patients,
        doctors=doctors
    )


@app.route("/add_appointment", methods=["POST"])
def add_appointment():
    new_appointment = Appointment(
        patient_id=request.form["patient_id"],
        doctor_id=request.form["doctor_id"],
        appointment_date=datetime.strptime(
            request.form["appointment_date"], "%Y-%m-%d"
        ),
        status=request.form["status"]
    )
    db.session.add(new_appointment)
    db.session.commit()
    return redirect(url_for("view_appointments"))


@app.route("/delete_appointment/<int:id>")
def delete_appointment(id):
    appointment = Appointment.query.get(id)
    db.session.delete(appointment)
    db.session.commit()
    return redirect(url_for("view_appointments"))


# ============================================================
# BILLING CRUD
# ============================================================

@app.route("/billing")
def view_billing():
    bills = Billing.query.all()
    patients = Patient.query.all()
    return render_template(
        "billing.html",
        bills=bills,
        patients=patients
    )


@app.route("/add_bill", methods=["POST"])
def add_bill():
    new_bill = Billing(
        patient_id=request.form["patient_id"],
        amount=request.form["amount"],
        payment_status=request.form["payment_status"]
    )
    db.session.add(new_bill)
    db.session.commit()
    return redirect(url_for("view_billing"))


@app.route("/delete_bill/<int:id>")
def delete_bill(id):
    bill = Billing.query.get(id)
    db.session.delete(bill)
    db.session.commit()
    return redirect(url_for("view_billing"))


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)