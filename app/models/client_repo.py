from app.core.db import get_conn

class ClientRepository:
    @staticmethod
    def list_clients_with_counts():
        """
        Returns list of clients ordered by Name ASC with:
        - name (left aligned in UI)
        - code (left aligned in UI)
        - linked_contacts count (integer, center in UI)
        """
        conn = get_conn()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("""
                SELECT cl.id, cl.name, cl.code, COUNT(cc.contact_id) AS linked_contacts
                FROM clients cl
                LEFT JOIN client_contact cc ON cc.client_id = cl.id
                GROUP BY cl.id, cl.name, cl.code
                ORDER BY cl.name ASC;
            """)
            return cur.fetchall()
        finally:
            conn.close()

    @staticmethod
    def list_clients():
        """
        Backwards-compatible method (optional).
        If you want, you can remove this and update all calls to list_clients_with_counts().
        """
        conn = get_conn()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT id, name, code FROM clients ORDER BY name ASC;")
            return cur.fetchall()
        finally:
            conn.close()

    @staticmethod
    def get_client(client_id: int):
        conn = get_conn()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT id, name, code FROM clients WHERE id=%s;", (client_id,))
            return cur.fetchone()
        finally:
            conn.close()

    @staticmethod
    def create_client(name: str, code: str) -> int:
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO clients (name, code) VALUES (%s, %s);", (name, code))
            conn.commit()
            return cur.lastrowid
        except:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def update_client(client_id: int, name: str):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("UPDATE clients SET name=%s WHERE id=%s;", (name, client_id))
            conn.commit()
        except:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def max_numeric_for_prefix(prefix: str) -> int:
        """
        Returns max numeric part used for codes like PREFIX###.
        """
        conn = get_conn()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute(
                """
                SELECT MAX(CAST(SUBSTRING(code,4,3) AS UNSIGNED)) AS max_num
                FROM clients
                WHERE code LIKE CONCAT(%s, '%%');
                """,
                (prefix,)
            )
            row = cur.fetchone()
            return int(row["max_num"] or 0)
        finally:
            conn.close()
