from flask import Flask, render_template, request, redirect, url_for, flash, session, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import csv
import io

app = Flask(__name__)
app.secret_key = "security_manpower_secret_key"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Table 1: Client Procurement Pipeline
class ManpowerRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    service_type = db.Column(db.String(50), nullable=False)
    staff_count = db.Column(db.Integer, nullable=False)
    details = db.Column(db.Text, nullable=True)

# Table 2: Recruitment Applications
class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    applicant_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    role_applied = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text, nullable=True)

# NEW TABLE 3: Operational Staff Shift Attendance Logs
class AttendanceLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staff_name = db.Column(db.String(100), nullable=False)
    action_type = db.Column(db.String(20), nullable=False) # Check-In or Check-Out
    timestamp = db.Column(db.DateTime, default=datetime.now)
    location_tag = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/request-staff", methods=["GET", "POST"])
def request_staff():
    if request.method == "POST":
        new_request = ManpowerRequest(
            client_name=request.form.get("name"),
            email=request.form.get("email"),
            service_type=request.form.get("service_type"),
            staff_count=int(request.form.get("staff_count", 1)),
            details=request.form.get("details")
        )
        db.session.add(new_request)
        db.session.commit()
        flash("Your request has been saved permanently to our database!", "success")
        return redirect(url_for("request_staff"))
    return render_template("request_staff.html")

@app.route("/careers", methods=["GET", "POST"])
def careers():
    if request.method == "POST":
        new_applicant = JobApplication(
            applicant_name=request.form.get("applicant_name"),
            phone=request.form.get("phone"),
            experience=int(request.form.get("experience", 0)),
            role_applied=request.form.get("role_applied"),
            notes=request.form.get("notes")
        )
        db.session.add(new_applicant)
        db.session.commit()
        flash("Application submitted successfully!", "success")
        return redirect(url_for("careers"))
    return render_template("careers.html")

# --- NEW: MOBILE GUARD ATTENDANCE TERMINAL ---
@app.route("/attendance", methods=["GET", "POST"])
def attendance():
    if request.method == "POST":
        log_entry = AttendanceLog(
            staff_name=request.form.get("staff_name"),
            action_type=request.form.get("action_type"),
            location_tag=request.form.get("location_tag", "Main Site Operational")
        )
        db.session.add(log_entry)
        db.session.commit()
        flash(f"Status logged successfully: {log_entry.action_type} at {datetime.now().strftime('%H:%M')}", "success")
        return redirect(url_for("attendance"))
    return render_template("attendance.html")

# --- NEW: ADMIN INVOICE GENERATOR ROUTE ---
@app.route("/admin-invoice", methods=["GET", "POST"])
def admin_invoice():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
        
    all_leads = ManpowerRequest.query.all()
    selected_invoice = None
    
    if request.method == "POST":
        lead_id = int(request.form.get("lead_id", 0))
        rate_per_head = float(request.form.get("rate_per_head", 0))
        duration_days = int(request.form.get("duration_days", 1))
        
        target_lead = ManpowerRequest.query.get(lead_id)
        if target_lead:
            total_cost = target_lead.staff_count * rate_per_head * duration_days
            selected_invoice = {
                "client_name": target_lead.client_name,
                "service_type": target_lead.service_type,
                "staff_count": target_lead.staff_count,
                "rate": rate_per_head,
                "days": duration_days,
                "total": round(total_cost, 2),
                "invoice_number": f"DSDM-{1000 + target_lead.id}"
            }
            
    return render_template("admin_invoice.html", leads=all_leads, invoice=selected_invoice)

@app.route("/payroll", methods=["GET", "POST"])
def payroll():
    if "ledger" not in session: session["ledger"] = []
    payroll_result = None
    if request.method == "POST":
        try:
            name = request.form.get("staff_name")
            hourly_rate = float(request.form.get("hourly_rate", 0))
            hours_worked = float(request.form.get("hours_worked", 0))
            if hours_worked > 40:
                gross_pay = (40 * hourly_rate) + ((hours_worked - 40) * hourly_rate * 1.5)
            else:
                gross_pay = hours_worked * hourly_rate
            payroll_result = {"staff_name": name, "gross_pay": f"{round(gross_pay, 2)}"}
            current_ledger = list(session["ledger"])
            current_ledger.append({"name": name, "hours": hours_worked, "pay": f"{round(gross_pay, 2)}"})
            session["ledger"] = current_ledger
        except ValueError: flash("Enter valid numbers.", "danger")
    return render_template("payroll.html", result=payroll_result, session_ledger=session["ledger"])

@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form.get("username") == "admin" and request.form.get("password") == "dsdmatwar123":
            session["admin_logged_in"] = True
            return redirect(url_for("admin_dashboard"))
        else: flash("Invalid credentials.", "danger")
    return render_template("admin_login.html")

@app.route("/admin-dashboard")
def admin_dashboard():
    if not session.get("admin_logged_in"): return redirect(url_for("admin_login"))
    all_leads = ManpowerRequest.query.all()
    all_applicants = JobApplication.query.all()
    all_attendance = AttendanceLog.query.order_by(AttendanceLog.timestamp.desc()).all()
    return render_template("admin_dashboard.html", leads=all_leads, applicants=all_applicants, attendance=all_attendance)

if __name__ == "__main__":
    app.run(debug=True)
