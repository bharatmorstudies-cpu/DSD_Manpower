# 🛡️ Security & Manpower Supply Business Website

A robust, secure, and professional web application built using Python to showcase premium security services and corporate manpower solutions. This platform allows clients to explore staffing services, request security personnel, and submit hiring inquiries.

---

## 🌟 Key Features

* **Service Catalog**: Detailed overviews of Guarding, Executive Protection, Event Security, and Facility Management.
* **Manpower Request Portal**: Interactive forms for corporate clients to submit specific staffing needs.
* **Job Application Portal**: A dedicated recruitment page for job seekers to upload resumes and apply for roles.
* **Admin Dashboard**: Secure backend for management to view incoming client leads and applicant data.
* **Contact & Quotation Engine**: Automatic email notifications for quick client bidding and quotes.

---

## 🛠️ Tech Stack

* **Backend**: Python 3.11+ with [Flask](https://palletsprojects.com) (or [Django](https://djangoproject.com))
* **Frontend**: HTML5, CSS3, JavaScript, and Bootstrap 5 (Responsive Layout)
* **Database**: SQLite (Development) / PostgreSQL (Production)
* **Authentication**: Flask-Login / Django Auth (Secure admin panel)

---

## ⚙️ Installation & Setup

Follow these steps to run the website locally on your machine.

### 1. Clone the Repository
```bash
git clone https://github.com
cd security-manpower-website
```

### 2. Set Up a Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
# For Flask application
python app.py
```
The website will be live at `http://127.0.0`.

---

## 📂 Project Structure

```text
├── static/                  # CSS, JavaScript, and corporate images
├── templates/               # HTML layout files (Home, Services, Careers, Contact)
├── app.py                   # Main Python application router and logic
├── models.py                # Database schemas (Leads, Applicants, Users)
├── requirements.txt         # List of Python library dependencies
└── README.md                # Project documentation
```

---

## 🔒 Security Practices Built-in

* **CSRF Protection**: All client request forms are protected against Cross-Site Request Forgery.
* **Input Validation**: Strict server-side verification for phone numbers, emails, and resume file types.
* **SQL Injection Prevention**: Built using Object-Relational Mapping (ORM) to handle queries securely.
