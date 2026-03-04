from flask import jsonify

def ok(message="", **extra):
    payload = {"success": True, "message": message}
    payload.update(extra)
    return jsonify(payload), 200

def fail(message="", status=400, **extra):
    payload = {"success": False, "message": message}
    payload.update(extra)
    return jsonify(payload), status
