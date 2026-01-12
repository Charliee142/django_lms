# django_lms
Django Learning Management System (LMS)

Description
===========
This project is a full-featured Learning Management System (LMS) built with Django.
It allows instructors to create and manage courses while enabling students to enroll, learn, track progress, and earn certificates — all in a secure and scalable web platform.

The system follows real-world LMS architecture, supporting role-based access control, course categorization, modular learning, and secure authentication.

Problem it Solves
=================
Many online learning platforms are:

Expensive to customize

Difficult to self-host

Insecure or poorly structured

Not tailored for African institutions, academies, or independent instructors

This LMS solves these problems by:

Providing a self-hosted, customizable LMS

Supporting instructor–student separation

Offering secure authentication & access control

Enabling scalable course management

Features
========
👤 User Management

User registration & login

Role-based access (Admin, Instructor, Student)

Secure authentication

Profile management
🎓 Course Management

Create, update, and delete courses

Course categories & slugs

Course thumbnails and descriptions

Instructor ownership of courses

📚 Learning System

Lessons & modules

Course enrollment system

Student progress tracking

Course completion status
📜 Certificates

Automatic certificate generation

Issued after course completion

🔐 Access Control

Restricted instructor dashboards

Student-only course access

Admin-only management views

⚙️ Admin Dashboard

Manage users

Manage courses and categories

Monitor platform activities

Tech Stack
=========
Backend

Python

Django

Django ORM

Frontend

HTML5

CSS3

Bootstrap

Database

SQLite (Development)

PostgreSQL (Production-ready)

Authentication & Security

Django Authentication System

Role-based permissions

CSRF protection

Security Measures

Django CSRF protection

Password hashing

Role-based access control using decorators

Secure form validation

Slug-based URLs to prevent ID enumeration

Django Admin access restrictions

Screenshots / Demo
==================

(Dashboard, Course Pages, Enrollment Flow, Admin Panel)

<img width="960" height="540" alt="Screenshot 2025-05-17 155353" src="https://github.com/user-attachments/assets/a3ad7d60-0139-4dc3-9588-d73d75ec2a48" />
<img width="960" height="540" alt="Screenshot 2025-05-17 155441" src="https://github.com/user-attachments/assets/5f2cd911-39a5-4c49-8b2c-75eaaa1b8499" />
<img width="960" height="540" alt="Screenshot 2025-05-17 155535" src="https://github.com/user-attachments/assets/470b8414-97c5-4ffd-82d5-2beae599a3be" />
<img width="960" height="540" alt="Screenshot 2025-05-17 155718" src="https://github.com/user-attachments/assets/0096e597-45bd-4644-944f-b4c06c8af197" />
<img width="960" height="540" alt="Screenshot 2025-05-17 155807" src="https://github.com/user-attachments/assets/db473ead-28e9-4cfd-a631-b5a9c97871cb" />
<img width="960" height="540" alt="Screenshot 2025-05-17 155839" src="https://github.com/user-attachments/assets/d056bde3-5b98-4c85-b011-daf3f79cd61b" />
<img width="960" height="540" alt="Screenshot 2025-05-17 155906" src="https://github.com/user-attachments/assets/1f406b7a-eaf3-4dc9-b58c-b312f9833042" />
<img width="960" height="540" alt="Screenshot 2025-05-17 155936" src="https://github.com/user-attachments/assets/b623db8e-3578-459b-ad9f-6545c283357e" />
<img width="960" height="540" alt="Screenshot 2025-05-17 160004" src="https://github.com/user-attachments/assets/7eb56b43-a836-434a-82fe-12f9be96aa05" />
<img width="960" height="540" alt="Screenshot 2025-05-17 160028" src="https://github.com/user-attachments/assets/43582951-7bc3-4e3c-abb5-8370b2c0cb05" />
<img width="960" height="540" alt="Screenshot 2025-05-17 160116" src="https://github.com/user-attachments/assets/4f2433b8-ac7c-4f7a-9b48-e84ad411c0e8" />
<img width="960" height="540" alt="Screenshot 2025-05-17 160216" src="https://github.com/user-attachments/assets/a3db6ec1-b14d-4096-9d7f-f2cb29e24933" />
<img width="960" height="540" alt="Screenshot 2025-05-17 160243" src="https://github.com/user-attachments/assets/5e80fbd0-fb85-4272-b53a-e6bea9c80413" />
<img width="960" height="540" alt="Screenshot 2025-05-17 160321" src="https://github.com/user-attachments/assets/00848cc0-27a2-4e29-953a-67022017ca1e" />
<img width="960" height="540" alt="Screenshot 2025-05-17 160426" src="https://github.com/user-attachments/assets/4376f742-f173-4af3-8c11-79032f412cc8" />
<img width="960" height="540" alt="Screenshot 2025-05-17 160545" src="https://github.com/user-attachments/assets/c0382945-2fa4-4ded-a1b2-2120fa53ae94" />
<img width="960" height="540" alt="Screenshot 2025-05-17 160646" src="https://github.com/user-attachments/assets/8d56fbec-4665-4f1d-a225-44afff3f7ee1" />
<img width="960" height="540" alt="Screenshot 2025-05-17 160710" src="https://github.com/user-attachments/assets/e4721c4c-673d-40bb-a0b2-dc51099f2b6a" />
<img width="960" height="540" alt="Screenshot 2025-05-17 160738" src="https://github.com/user-attachments/assets/442dc868-db19-4f67-a86c-58be9d8ca12a" />
<img width="960" height="540" alt="Screenshot 2025-05-17 160810" src="https://github.com/user-attachments/assets/51e0f1ef-cc65-4716-8e86-09a6209ed78f" />
<img width="960" height="540" alt="Screenshot 2025-05-17 160831" src="https://github.com/user-attachments/assets/a755af11-f919-4d0f-ae3b-605b1b4e9e20" />
<img width="960" height="540" alt="Screenshot 2025-05-17 160933" src="https://github.com/user-attachments/assets/56ca709e-2ea4-441f-9886-9e28994bf9d6" />
<img width="960" height="540" alt="Screenshot 2025-05-17 161000" src="https://github.com/user-attachments/assets/4d18c8e9-c3ce-46b4-b918-e9485a77134a" />
<img width="960" height="540" alt="Screenshot 2025-05-17 161018" src="https://github.com/user-attachments/assets/c7b1860f-4854-4cdd-8cc0-4799f4f93f38" />
<img width="960" height="540" alt="Screenshot 2025-05-17 161046" src="https://github.com/user-attachments/assets/7b61f97b-18dd-4079-a618-a13e5cc7beb3" />
<img width="960" height="540" alt="Screenshot 2025-05-17 161115" src="https://github.com/user-attachments/assets/a9495ca6-592e-427b-a765-43e2afcdf0b5" />
<img width="960" height="540" alt="Screenshot 2025-05-17 161149" src="https://github.com/user-attachments/assets/a3b6a02e-90fd-45bf-9432-42a3d86def38" />
<img width="960" height="540" alt="Screenshot 2025-05-17 161214" src="https://github.com/user-attachments/assets/6e398a21-c22f-44e8-8dbd-47ee09845cb4" />
<img width="960" height="540" alt="Screenshot 2025-05-17 161252" src="https://github.com/user-attachments/assets/858e61e3-3bc8-44fb-bfa2-c8cea5b4bab5" />
<img width="960" height="540" alt="Screenshot 2025-05-17 161313" src="https://github.com/user-attachments/assets/96a7b5e5-de66-4214-87d7-b5b195024cc0" />
<img width="960" height="540" alt="Screenshot 2025-05-17 161400" src="https://github.com/user-attachments/assets/86d16d66-db9b-4ad4-bc91-081fe5f7298c" />
<img width="960" height="540" alt="Screenshot 2025-05-17 161431" src="https://github.com/user-attachments/assets/d425911e-73b9-4d77-9fb3-54a71b64ee3e" />
<img width="960" height="540" alt="Screenshot 2025-05-17 161455" src="https://github.com/user-attachments/assets/ce558eeb-71fa-4ba9-890c-937887a7cb8c" />
<img width="960" height="540" alt="Screenshot 2025-05-17 161520" src="https://github.com/user-attachments/assets/353247c8-a482-462a-aee8-58edf0d13f17" />
<img width="960" height="540" alt="Screenshot 2025-05-17 161547" src="https://github.com/user-attachments/assets/565b3685-e243-4cc1-b70c-63a89148ed91" />
<img width="960" height="540" alt="Screenshot 2025-05-17 161613" src="https://github.com/user-attachments/assets/d05b27b4-b9b5-4cd8-b882-aa4a30e87883" />
<img width="960" height="540" alt="Screenshot 2025-05-17 161636" src="https://github.com/user-attachments/assets/b76111ec-a946-45c4-8317-099243c4a48c" />

Installation
============
1. Clone the Repository
git clone https://github.com/Charliee142/django_lms.git
cd django_lms
2. Create Virtual Environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
3. Install Dependencies
pip install -r requirements.txt
4. Run Migrations
python manage.py makemigrations
python manage.py migrate
5. Create Superuser
python manage.py createsuperuser
6. Run the Server
python manage.py runserver
Open:

http://127.0.0.1:8000/

What I Learned
==============
Designing a real-world LMS architecture

Django model relationships (ForeignKey, OneToOne)

Role-based access control with decorators

Handling migrations and schema evolution

Secure authentication & authorization

Structuring scalable Django applications

Debugging Django migration issues

Preparing production-ready projects for GitHub
