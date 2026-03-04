from flask import Flask, redirect, url_for
from config import Config
from app.controllers.client_controller import client_bp
from app.controllers.contact_controller import contact_bp
from app.controllers.link_controller import link_bp

def create_app():
    flask_app = Flask(__name__, static_folder="app/views/static", template_folder="app/views/templates")
    flask_app.config.from_object(Config)

    flask_app.register_blueprint(client_bp)
    flask_app.register_blueprint(contact_bp)
    flask_app.register_blueprint(link_bp)

    @flask_app.get("/")
    def home():
        return redirect(url_for("clients.list_clients"))

    return flask_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
