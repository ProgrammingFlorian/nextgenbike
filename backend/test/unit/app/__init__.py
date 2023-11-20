import pytest
from app import create_app
from app.extensions import db


@pytest.fixture
def client():
    client = create_app()
    with client.app_context():
        yield client.test_client()
