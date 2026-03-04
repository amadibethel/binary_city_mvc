import mysql.connector
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.core.validator import required
from app.core.client_code import make_prefix, format_code
from app.models.client_repo import ClientRepository
from app.models.link_repo import LinkRepository

client_bp = Blueprint("clients", __name__, url_prefix="/clients")

@client_bp.get("")
def list_clients():
    clients = ClientRepository.list_clients()
    return render_template("clients_list.html", clients=clients)

@client_bp.get("/new")
def new_client():
    # New client: no code shown
    return render_template("client_form.html", client=None, contacts=[], unlinked_contacts=[])

@client_bp.post("")
def create_client():
    name = (request.form.get("name") or "").strip()
    if not required(name):
        flash("Client Name is required.", "error")
        return redirect(url_for("clients.new_client"))

    prefix = make_prefix(name)
    next_num = ClientRepository.max_numeric_for_prefix(prefix) + 1
    code = format_code(prefix, next_num)

    # Safety: handle rare collisions via retry
    for _ in range(5):
        try:
            client_id = ClientRepository.create_client(name=name, code=code)
            flash("Client created successfully.", "success")
            return redirect(url_for("clients.edit_client", client_id=client_id))
        except mysql.connector.IntegrityError:
            next_num += 1
            code = format_code(prefix, next_num)

    flash("Could not generate a unique client code. Please try again.", "error")
    return redirect(url_for("clients.new_client"))

@client_bp.get("/<int:client_id>")
def edit_client(client_id: int):
    client = ClientRepository.get_client(client_id)
    if not client:
        flash("Client not found.", "error")
        return redirect(url_for("clients.list_clients"))

    contacts = LinkRepository.contacts_for_client(client_id)
    unlinked_contacts = LinkRepository.unlinked_contacts_for_client(client_id)

    return render_template(
        "client_form.html",
        client=client,
        contacts=contacts,
        unlinked_contacts=unlinked_contacts
    )

@client_bp.post("/<int:client_id>")
def update_client(client_id: int):
    client = ClientRepository.get_client(client_id)
    if not client:
        flash("Client not found.", "error")
        return redirect(url_for("clients.list_clients"))

    name = (request.form.get("name") or "").strip()
    if not required(name):
        flash("Client Name is required.", "error")
        return redirect(url_for("clients.edit_client", client_id=client_id))

    ClientRepository.update_client(client_id, name)
    flash("Client updated successfully.", "success")
    return redirect(url_for("clients.edit_client", client_id=client_id))
