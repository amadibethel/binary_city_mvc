## Client/Contact MVC (Python + MySQL)

### Features

- Clients & Contacts CRUD
- Client Code auto-generation (3 letters + 3 digits), unique, increments from 001
- Many-to-many linking via junction table
- Tabbed forms: General + Contact(s)/Client(s)
- AJAX link/unlink actions
- Server-side validation for required fields + email validity + email uniqueness

### Setup

1) Create DB and tables:
- Open `database/schema.sql` in MySQL and run it.

2) Create virtual env + install:
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt

3) Configure environment (optional):
Create .env in project root:

SECRET_KEY=super-secret
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=yourpassword
MYSQL_DATABASE=client_contact_db

4) Run:

python app.py

