import pytest
from app import create_app, db
from app.models import Message

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_messages(client):
    # Add a sample message
    from app.models import Message
    from app import db
    with client.application.app_context():
        msg = Message(username='Ian', body='Hello!')
        db.session.add(msg)
        db.session.commit()
    
    # Test GET /messages
    res = client.get('/messages')
    assert res.status_code == 200
    data = res.get_json()
    assert data[0]["username"] == "Ian"
    assert data[0]["body"] == "Hello!"
