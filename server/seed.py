# server/seed.py

from app import create_app, db
from server.app.models import Message
from datetime import datetime

# Create the Flask app using the factory
app = create_app()

# Use the app context so SQLAlchemy knows which app to work with
with app.app_context():
    # Drop existing tables (if any) and create new ones
    db.drop_all()
    db.create_all()

    # Seed sample messages
    messages = [
        Message(username="Alice", body="Hello!", created_at=datetime.utcnow()),
        Message(username="Bob", body="Hi there!", created_at=datetime.utcnow()),
        Message(username="Charlie", body="How's it going?", created_at=datetime.utcnow())
    ]

    # Add messages to the session and commit
    db.session.add_all(messages)
    db.session.commit()

    print("Database seeded successfully")
