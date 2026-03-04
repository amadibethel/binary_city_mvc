from app.core.db import get_conn

class ContactRepository:
    @staticmethod
    def list_contacts_with_counts():
        conn = get_conn()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("""
                SELECT c.id, c.name, c.surname, c.email, COUNT(cc.client_id) AS linked_clients
                FROM contacts c
                LEFT JOIN client_contact cc ON cc.contact_id = c.id
                GROUP BY c.id, c.name, c.surname, c.email
                ORDER BY c.surname ASC, c.name ASC;
            """)
            return cur.fetchall()
        finally:
            conn.close()

    @staticmethod
    def get_contact(contact_id: int):
        conn = get_conn()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT id, name, surname, email FROM contacts WHERE id=%s;", (contact_id,))
            return cur.fetchone()
        finally:
            conn.close()

    @staticmethod
    def create_contact(name: str, surname: str, email: str) -> int:
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO contacts (name, surname, email) VALUES (%s, %s, %s);",
                (name, surname, email)
            )
            conn.commit()
            return cur.lastrowid
        except:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def update_contact(contact_id: int, name: str, surname: str, email: str):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "UPDATE contacts SET name=%s, surname=%s, email=%s WHERE id=%s;",
                (name, surname, email, contact_id)
            )
            conn.commit()
        except:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def email_exists(email: str, exclude_contact_id: int | None = None) -> bool:
        conn = get_conn()
        try:
            cur = conn.cursor()
            if exclude_contact_id:
                cur.execute("SELECT 1 FROM contacts WHERE email=%s AND id<>%s LIMIT 1;", (email, exclude_contact_id))
            else:
                cur.execute("SELECT 1 FROM contacts WHERE email=%s LIMIT 1;", (email,))
            return cur.fetchone() is not None
        finally:
            conn.close()
