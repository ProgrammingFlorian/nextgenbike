import pytest
from server.server import create_app
from server.server import db


@pytest.fixture
def client():
    client = create_app()
    with client.app_context():
        db.create_all()
        yield client.test_client()
        db.drop_all()
