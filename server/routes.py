from flask import Blueprint, request, jsonify
from server.app.models import Message
from app import create_app, db

main_routes = Blueprint("main_routes", __name__)

@main_routes.route("/messages", methods=["GET"])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([m.to_dict() for m in messages]), 200

@main_routes.route("/messages", methods=["POST"])
def create_message():
    data = request.get_json()
    new_msg = Message(body=data.get("body"), username=data.get("username"))
    db.session.add(new_msg)
    db.session.commit()
    return jsonify(new_msg.to_dict()), 201

@main_routes.route("/messages/<int:id>", methods=["PATCH"])
def update_message(id):
    data = request.get_json()
    msg = Message.query.get_or_404(id)
    if "body" in data:
        msg.body = data["body"]
    db.session.commit()
    return jsonify(msg.to_dict()), 200

@main_routes.route("/messages/<int:id>", methods=["DELETE"])
def delete_message(id):
    msg = Message.query.get_or_404(id)
    db.session.delete(msg)
    db.session.commit()
    return jsonify({"message": "Deleted successfully"}), 200
