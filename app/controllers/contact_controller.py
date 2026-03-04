import mysql.connector
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.core.validator import required, is_email
from app.models.contact_repo import ContactRepository
from app.models.link_repo import LinkRepository

contact_bp = Blueprint("contacts", __name__, url_prefix="/contacts")

@contact_bp.get("")
def list_contacts():
    contacts = ContactRepository.list_contacts_with_counts()
    return render_template("contacts_list.html", contacts=contacts)

@contact_bp.get("/new")
def new_contact():
    return render_template("contact_form.html", contact=None, clients=[], unlinked_clients=[])

@contact_bp.post("")
def create_contact():
    name = (request.form.get("name") or "").strip()
    surname = (request.form.get("surname") or "").strip()
    email = (request.form.get("email") or "").strip()

    errors = []
    if not required(name): errors.append("Name is required.")
    if not required(surname): errors.append("Surname is required.")
    if not required(email): errors.append("Email is required.")
    elif not is_email(email): errors.append("Email must be a valid email address.")
    elif ContactRepository.email_exists(email): errors.append("Email must be unique for all contacts.")

    if errors:
        for e in errors: flash(e, "error")
        return redirect(url_for("contacts.new_contact"))

    try:
        contact_id = ContactRepository.create_contact(name, surname, email)
        flash("Contact created successfully.", "success")
        return redirect(url_for("contacts.edit_contact", contact_id=contact_id))
    except mysql.connector.IntegrityError:
        flash("Email must be unique for all contacts.", "error")
        return redirect(url_for("contacts.new_contact"))

@contact_bp.get("/<int:contact_id>")
def edit_contact(contact_id: int):
    contact = ContactRepository.get_contact(contact_id)
    if not contact:
        flash("Contact not found.", "error")
        return redirect(url_for("contacts.list_contacts"))

    clients = LinkRepository.clients_for_contact(contact_id)
    unlinked_clients = LinkRepository.unlinked_clients_for_contact(contact_id)

    return render_template(
        "contact_form.html",
        contact=contact,
        clients=clients,
        unlinked_clients=unlinked_clients
    )

@contact_bp.post("/<int:contact_id>")
def update_contact(contact_id: int):
    contact = ContactRepository.get_contact(contact_id)
    if not contact:
        flash("Contact not found.", "error")
        return redirect(url_for("contacts.list_contacts"))

    name = (request.form.get("name") or "").strip()
    surname = (request.form.get("surname") or "").strip()
    email = (request.form.get("email") or "").strip()

    errors = []
    if not required(name): errors.append("Name is required.")
    if not required(surname): errors.append("Surname is required.")
    if not required(email): errors.append("Email is required.")
    elif not is_email(email): errors.append("Email must be a valid email address.")
    elif ContactRepository.email_exists(email, exclude_contact_id=contact_id): errors.append("Email must be unique for all contacts.")

    if errors:
        for e in errors: flash(e, "error")
        return redirect(url_for("contacts.edit_contact", contact_id=contact_id))

    try:
        ContactRepository.update_contact(contact_id, name, surname, email)
        flash("Contact updated successfully.", "success")
    except mysql.connector.IntegrityError:
        flash("Email must be unique for all contacts.", "error")

    return redirect(url_for("contacts.edit_contact", contact_id=contact_id))
