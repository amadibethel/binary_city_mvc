# Client & Contact Management System (Python + MySQL MVC)

A lightweight **Client and Contact Management Web Application** built with **Python (Flask)** and **MySQL**, following an **MVC architecture**.

The system allows users to:

- Manage **Clients**
- Manage **Contacts**
- Create **many-to-many relationships** between clients and contacts
- Automatically generate **unique Client Codes**
- View linked relationships with proper ordering and validation

---

# Project Overview

The application provides two main modules:

## Clients

Users can:
- Create new clients
- View all clients ordered by **Name ascending**
- View the **number of linked contacts**
- View and edit client details
- Link contacts to a client
- Unlink contacts from a client

Example Client Codes:

| Client Name | Code |
|-------------|------|
| First National Bank | FNB001 |
| Protea | PRO001 |
| IT | ITA001 |

---

## Contacts

Users can:
- Create contacts
- View contacts ordered by **Surname Name**
- View number of linked clients
- Link clients to contacts
- Unlink clients from contacts

---

# Client Code Generation

Each client receives a **unique 6‑character code**:

AAA999

AAA = three uppercase letters  
999 = numeric sequence starting from **001**

Rules:

1. Multi‑word name, first letters of first 3 words  
   Example: First National Bank **FNB001**

2. Single word first 3 letters  
   Example: Protea **PRO001**

3. If fewer than 3 letters fill using A‑Z  
   Example: IT → **ITA001**

4. Numbers increment sequentially:

PRO001, PRO002, PRO003

---

# Technology Stack

Backend: Python (Flask)  
Database: MySQL  
Architecture: MVC  
Templates: Jinja2  
Frontend: HTML / CSS / JavaScript  
AJAX: Fetch API

---

# Project Structure

client_contact_mvc

app.py  
config.py  
requirements.txt  

database/  
schema.sql  

app/  

core/  
db.py  
validator.py  
response.py  
client_code.py  

controllers/  
client_controller.py  
contact_controller.py  
link_controller.py  

models/  
client_repo.py  
contact_repo.py  
link_repo.py  

views/  

templates/  
layout.html  
clients_list.html  
client_form.html  
contacts_list.html  
contact_form.html  

static/  
app.js  
styles.css  

---

# Database Design

## Clients Table

id INT PRIMARY KEY  
name VARCHAR  
code CHAR(6) UNIQUE  
created_at DATETIME

## Contacts Table

id INT PRIMARY KEY  
name VARCHAR  
surname VARCHAR  
email VARCHAR UNIQUE  
created_at DATETIME

## Client_Contact Table

client_id INT  
contact_id INT  
PRIMARY KEY (client_id, contact_id)

This creates the **many‑to‑many relationship**.

---

# Installation

## 1 Clone Repository

git clone <repo-url>  
cd client_contact_mvc

## 2 Create Virtual Environment

Windows

python -m venv venv  
venv\Scripts\activate

Mac/Linux

python3 -m venv venv  
source venv/bin/activate

## 3 Install Dependencies

pip install -r requirements.txt

## 4 Create Database

Run:

mysql -u root -p < database/schema.sql

## 5 Configure Environment

Create `.env`

SECRET_KEY=super-secret  
MYSQL_HOST=127.0.0.1  
MYSQL_PORT=3306  
MYSQL_USER=root  
MYSQL_PASSWORD=password  
MYSQL_DATABASE=client_contact_db  

## 6 Run Application

python app.py

Open in browser:

http://127.0.0.1:5000

---

# Validation

Server-side validation checks:

- Required fields
- Email format
- Email uniqueness
- Unique client codes

Client-side JavaScript handles:

- AJAX linking/unlinking
- Tab switching
- UI updates

---

# Security

- Parameterized SQL queries
- Server-side validation
- Unique database constraints

---

# Future Improvements

- Search
- Pagination
- REST API
- Authentication
- UI framework
- Automated tests

---

# Author

Bethel Amadi

Developed as part of a **Software Development Practical Assessment** demonstrating:

- Python backend development
- SQL database design
- MVC architecture
- Web application development

