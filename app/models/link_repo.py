from app.core.db import get_conn

class LinkRepository:
    # --- Client -> Contacts ---
    @staticmethod
    def contacts_for_client(client_id: int):
        conn = get_conn()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("""
                SELECT c.id, c.surname, c.name, c.email
                FROM contacts c
                JOIN client_contact cc ON cc.contact_id = c.id
                WHERE cc.client_id = %s
                ORDER BY c.surname ASC, c.name ASC;
            """, (client_id,))
            return cur.fetchall()
        finally:
            conn.close()

    @staticmethod
    def unlinked_contacts_for_client(client_id: int):
        conn = get_conn()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("""
                SELECT c.id, c.surname, c.name, c.email
                FROM contacts c
                WHERE c.id NOT IN (
                    SELECT contact_id FROM client_contact WHERE client_id = %s
                )
                ORDER BY c.surname ASC, c.name ASC;
            """, (client_id,))
            return cur.fetchall()
        finally:
            conn.close()

    @staticmethod
    def link_contact(client_id: int, contact_id: int):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO client_contact (client_id, contact_id) VALUES (%s, %s);", (client_id, contact_id))
            conn.commit()
        except:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def unlink_contact(client_id: int, contact_id: int):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM client_contact WHERE client_id=%s AND contact_id=%s;", (client_id, contact_id))
            conn.commit()
        except:
            conn.rollback()
            raise
        finally:
            conn.close()

    # --- Contact -> Clients ---
    @staticmethod
    def clients_for_contact(contact_id: int):
        conn = get_conn()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("""
                SELECT cl.id, cl.name, cl.code
                FROM clients cl
                JOIN client_contact cc ON cc.client_id = cl.id
                WHERE cc.contact_id = %s
                ORDER BY cl.name ASC;
            """, (contact_id,))
            return cur.fetchall()
        finally:
            conn.close()

    @staticmethod
    def unlinked_clients_for_contact(contact_id: int):
        conn = get_conn()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("""
                SELECT cl.id, cl.name, cl.code
                FROM clients cl
                WHERE cl.id NOT IN (
                    SELECT client_id FROM client_contact WHERE contact_id=%s
                )
                ORDER BY cl.name ASC;
            """, (contact_id,))
            return cur.fetchall()
        finally:
            conn.close()

    @staticmethod
    def link_client(contact_id: int, client_id: int):
        # same table; just reversed args
        return LinkRepository.link_contact(client_id=client_id, contact_id=contact_id)

    @staticmethod
    def unlink_client(contact_id: int, client_id: int):
        return LinkRepository.unlink_contact(client_id=client_id, contact_id=contact_id)
