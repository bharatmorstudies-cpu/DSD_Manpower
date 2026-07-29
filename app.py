from flask import Flask, render_template, request, redirect, url_for, flash, session, Response
from flask_sqlalchemy import SQLAlchemy
import os
import csv
import io

app = Flask(__name__)
app.secret_key = "security_manpower_secret_key"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Existing Table: Client Procurement Enquiries
class ManpowerRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    service_type = db.Column(db.String(50), nullable=False)
    staff_count = db.Column(db.Integer, nullable=False)
    details = db.Column(db.Text, nullable=True)

# NEW TABLE: Guard & Staff Recruitment Applications
class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    applicant_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    role_applied = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text, nullable=True)

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

# --- NEW CAREERS PORTAL ROUTE ---
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
        flash("Application submitted successfully! Our recruitment team will review your profile.", "success")
        return redirect(url_for("careers"))
    return render_template("careers.html")

@app.route("/payroll", methods=["GET", "POST"])
def payroll():
    if "ledger" not in session:
        session["ledger"] = []
        
    payroll_result = None
    if request.method == "POST":
        try:
            name = request.form.get("staff_name")
            hourly_rate = float(request.form.get("hourly_rate", 0))
            hours_worked = float(request.form.get("hours_worked", 0))
            
            if hours_worked > 40:
                reg_hours = 40
                ot_hours = hours_worked - 40
                gross_pay = (40 * hourly_rate) + (ot_hours * hourly_rate * 1.5)
            else:
                reg_hours = hours_worked
                ot_hours = 0
                gross_pay = hours_worked * hourly_rate
                
            payroll_result = {
                "staff_name": name,
                "reg_hours": reg_hours,
                "ot_hours": ot_hours,
                "gross_pay": f"{round(gross_pay, 2)}"
            }
            
            current_ledger = list(session["ledger"])
            current_ledger.append({"name": name, "hours": hours_worked, "pay": f"{round(gross_pay, 2)}"})
            session["ledger"] = current_ledger
            
        except ValueError:
            flash("Enter valid numbers.", "danger")
            
    return render_template("payroll.html", result=payroll_result, session_ledger=session["ledger"])

@app.route("/export-payroll")
def export_payroll():
    ledger = session.get("ledger", [])
    if not ledger:
        return redirect(url_for("payroll"))
        
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Staff Name", "Total Hours Logged", "Gross Payout"])
    
    for row in ledger:
        writer.writerow([row["name"], row["hours"], row["pay"]])
        
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=DSD_Matwar_Payroll_Export.csv"}
    )

@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form.get("username") == "admin" and request.form.get("password") == "dsdmatwar123":
            session["admin_logged_in"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Invalid administrator credentials.", "danger")
    return render_template("admin_login.html")

# --- UPDATED ADMIN DASHBOARD: SHOWS INQUIRIES & APPLICATIONS ---
@app.route("/admin-dashboard")
def admin_dashboard():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    all_leads = ManpowerRequest.query.all()
    all_applicants = JobApplication.query.all()
    return render_template("admin_dashboard.html", leads=all_leads, applicants=all_applicants)

@app.route("/admin-delete/<int:lead_id>")
def admin_delete(lead_id):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    lead_to_delete = ManpowerRequest.query.get_or_404(lead_id)
    db.session.delete(lead_to_delete)
    db.session.commit()
    flash("Inquiry record successfully removed.", "success")
    return redirect(url_for("admin_dashboard"))

# --- NEW: DELETE RECRUITMENT APPLICANT ---
@app.route("/admin-delete-applicant/<int:app_id>")
def admin_delete_applicant(app_id):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    app_to_delete = JobApplication.query.get_or_404(app_id)
    db.session.delete(app_to_delete)
    db.session.commit()
    flash("Application record successfully removed.", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin-logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
