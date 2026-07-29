# 🛡️ DSD & Matwar Security & Manpower Solutions

An enterprise-grade, secure, and responsive web application built using Python to streamline tier-1 security operations, corporate facility assets management, and administrative staffing pipelines. 

Live Deployment Link: https://pythonanywhere.com

---

## 🌟 Strategic Business Core Modules

### 1. 💼 Executive Procurement Intake Portal
* **Target Audience**: Corporate clients, commercial enterprises, and venue hubs.
* **Functionality**: Standardizes high-volume staffing requests for elite bouncers, security forces, and specialized facilities personnel. 
* **Persistence**: Automates lead logging directly into a relational backend database framework.

### 2. 👥 Integrated Recruitment Pipeline
* **Target Audience**: Field personnel and applicants seeking operational employment.
* **Functionality**: Provides a dedicated, frictionless landing node capturing vetting information, physical attributes, contact anchors, and tracking histories.

### 3. 📡 Mobile Duty Attendance Tracker
* **Target Audience**: Deployed field operators and security staff.
* **Functionality**: Mobile-optimized field terminal grouping **Check-In** and **Check-Out** punches onto a single row. It eliminates duplicate logging and automatically calculates cumulative shift durations.

### 4. 🧮 Operations Control Dashboard & Invoicing Engine
* **Target Audience**: Internal administrative management.
* **Functionality**: 
  * Password-protected workspace managing incoming leads and applications with instant confirmation logic.
  * Built-in **Wage Processing Calculator** tracking overtime margins at 1.5x scaling rates.
  * Direct **Invoice Engine** pulling client metrics from rows to generate corporate billing statements with a single click.
  * Structured **Excel/CSV Export Utilities** for payroll analytics.

---

## 🛠️ Technology Stack Architecture

* **Backend Framework**: Python 3.11+ / Flask Framework
* **Data Layer Management**: SQLite Engine utilizing Python SQLAlchemy ORM mapping classes.
* **Frontend Matrix**: Semantic HTML5, Embedded Custom CSS, and Jinja2 Templating Systems (Zero External CDN Dependency for 100% Offline Integrity).
* **Environment Core**: Python Session Cryptography & Flask Relational Context Layers.

---

## 📂 Project Architecture Mapping

```text
├── instance/
│   └── database.db          # Persistent Relational SQLite Database
├── templates/
│   ├── base.html            # Master Layout (Corporate Design Theme)
│   ├── home.html            # Corporate Showcase & Statistics Landing Node
│   ├── services.html        # Solutions Matrix & Operational FAQ Engine
│   ├── request_staff.html   # B2B Procurement Intake Form Card
│   ├── careers.html         # Application Intake Interface
│   ├── attendance.html      # Mobile Shift Check-In/Out Punch Terminal
│   ├── payroll.html         # Wage Processing Sheet with Excel Export
│   ├── admin_login.html     # Secure Gateway Access Panel
│   └── admin_dashboard.html # Central Command (Leads, Attendance Sheets)
├── app.py                   # Master Application Router, Math Logic, & API Points
└── README.md                # System Documentation Portfolio
```

---

## ⚙️ Local Development Environment Setup

Follow these steps to launch the ecosystem locally on your workstation.

### 1. Initialize and Clone the Working Directory
```bash
git clone https://github.com
cd DSD_Manpower
```

### 2. Set Up a Clean Virtual Workspace
```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Required Library Components
```powershell
python -m pip install flask flask-sqlalchemy
```

### 4. Boot Up the Native Development Server
```powershell
python app.py
```
The site will instantly launch locally at **`http://127.0.0.1:5000`**.

---

## 🔒 Enterprise Security Protocols Built-in

* **SQL Injection Mitigation**: Complete usage of Object-Relational Mapping (ORM) to treat inputs as parameters, neutralizing cross-site string injections.
* **State Encryption**: Secure cookies managed via encrypted secret tokens prevent data exposure.
* **Session Validation**: Enforces server-side authentication state validation on all admin and billing routes.
