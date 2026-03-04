import mysql.connector
from flask import Blueprint, request
from app.core.response import ok, fail
from app.models.link_repo import LinkRepository

link_bp = Blueprint("links", __name__)

# -------- Client -> Contact linking ----------
@link_bp.post("/clients/<int:client_id>/link-contact")
def link_contact(client_id: int):
    contact_id = request.form.get("contact_id", type=int)
    if not contact_id:
        return fail("contact_id is required.")

    try:
        LinkRepository.link_contact(client_id, contact_id)
        return ok("Contact linked successfully.")
    except mysql.connector.IntegrityError:
        return fail("This contact is already linked to the client.", status=409)

@link_bp.post("/clients/<int:client_id>/unlink-contact")
def unlink_contact(client_id: int):
    contact_id = request.form.get("contact_id", type=int)
    if not contact_id:
        return fail("contact_id is required.")
    LinkRepository.unlink_contact(client_id, contact_id)
    return ok("Contact unlinked successfully.")

# -------- Contact -> Client linking ----------
@link_bp.post("/contacts/<int:contact_id>/link-client")
def link_client(contact_id: int):
    client_id = request.form.get("client_id", type=int)
    if not client_id:
        return fail("client_id is required.")

    try:
        LinkRepository.link_client(contact_id, client_id)
        return ok("Client linked successfully.")
    except mysql.connector.IntegrityError:
        return fail("This client is already linked to the contact.", status=409)

@link_bp.post("/contacts/<int:contact_id>/unlink-client")
def unlink_client(contact_id: int):
    client_id = request.form.get("client_id", type=int)
    if not client_id:
        return fail("client_id is required.")
    LinkRepository.unlink_client(contact_id, client_id)
    return ok("Client unlinked successfully.")
