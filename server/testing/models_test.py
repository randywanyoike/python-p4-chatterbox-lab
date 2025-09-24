# server/testing/models_test.py

import pytest
from app import create_app, db
from app.models import Message

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # temporary DB for testing

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

def test_message_creation(client):
    # Create a new message in the database
    with client.application.app_context():
        msg = Message(username='Ian', body='Hello, World!')
        db.session.add(msg)
        db.session.commit()

        # Check the message exists
        retrieved = Message.query.first()
        assert retrieved.username == 'Ian'
        assert retrieved.body == 'Hello, World!'

def test_message_update(client):
    with client.application.app_context():
        msg = Message(username='Ian', body='Old body')
        db.session.add(msg)
        db.session.commit()

        msg.body = 'Updated body'
        db.session.commit()

        retrieved = Message.query.first()
        assert retrieved.body == 'Updated body'

def test_message_delete(client):
    with client.application.app_context():
        msg = Message(username='Ian', body='To be deleted')
        db.session.add(msg)
        db.session.commit()

        db.session.delete(msg)
        db.session.commit()

        retrieved = Message.query.all()
        assert len(retrieved) == 0
