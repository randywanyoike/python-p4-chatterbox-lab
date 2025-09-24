from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate = Migrate(app, db)

    # Import models here to register with SQLAlchemy
    from .models import Message

    # Define route
    @app.route("/messages")
    def get_messages():
        messages = Message.query.all()
        return jsonify([{"username": m.username, "body": m.body} for m in messages])

    return app
