import pytest
from app import create_app
from app.extensions import db


@pytest.fixture
def client():
    client = create_app()
    with client.app_context():
        db.create_all()
        yield client.test_client()
        db.drop_all()
