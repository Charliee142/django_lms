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
