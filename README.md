A comprehensive Django-based platform for managing technical events with multi-role support (Admin, Vendor, Regular User).

## Features

### User Roles
- *Admin*: Full system control, user management, and content approval
- *Vendor*: Product management and order fulfillment
- *Regular User*: Product browsing, cart management, and checkout

### Core Functionality
- Secure authentication system
- Product approval workflow
- Shopping cart and order processing
- Item request system
- Responsive Bootstrap 5 interface

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. *Clone and setup environment*
bash
git clone https://github.com/AyushPandey-09/event-management.git
cd event-management
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate


2. *Install dependencies*
bash
pip install -r requirements.txt


3. *Configure and run*
bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver


## Access

- Application: http://localhost:8000
- Admin: http://localhost:8000/admin

## Project Structure


event_management/
├── em_app/               # Main application
├── event_management/     # Project config
├── media/                # Uploads
├── static/               # Static files
├── templates/            # HTML templates
├── requirements.txt      # Dependencies
└── README.md             # This file


## Usage

1. *Admin*: Approve products and manage users via Admin Portal
2. *Vendor*: Add products and handle requests via Vendor Portal
3. *User*: Browse, cart, and checkout products

## License

MIT License

## Contact

project@example.com

---

Note: The system requires initial superuser setup for admin access.
