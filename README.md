# Leave Management System (Django)

A web-based **Leave Management System** built with Django. Employees can sign in, apply for leave and track the status of their requests, while managers/admins review and approve or reject them.

## Features

- **User authentication** – registration, login and logout using Django's authentication system.
- **Leave applications** – submit leave requests with leave type, date range and reason.
- **Request tracking** – view the history and current status (pending / approved / rejected) of your leave requests.
- **Approval workflow** – managers/admins review pending requests and approve or reject them.
- **Admin panel** – manage users and leave records through the Django admin.

## Tech stack

- Python 3 · Django
- SQLite (default; can be switched to PostgreSQL)
- Django templates (HTML/CSS)

## Project structure

```
Practicing-LMS/
├── authentication/              # sign-up, login, logout
├── leave_management_system/     # leave requests, approvals, views & templates
├── <project_package>/           # settings.py, urls.py, wsgi.py
└── manage.py
```

## Getting started

```bash
git clone https://github.com/ZeeshanRQ/Practicing-LMS.git
cd Practicing-LMS

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install django              # or: pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser and http://127.0.0.1:8000/admin/ for the admin panel.
