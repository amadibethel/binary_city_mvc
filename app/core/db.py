import mysql.connector
from flask import current_app

def get_conn():
    cfg = current_app.config
    return mysql.connector.connect(
        host=cfg["MYSQL_HOST"],
        port=cfg["MYSQL_PORT"],
        user=cfg["MYSQL_USER"],
        password=cfg["MYSQL_PASSWORD"],
        database=cfg["MYSQL_DATABASE"],
        autocommit=False
    )
