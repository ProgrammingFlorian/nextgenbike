import pytest
from server.app import create_app


@pytest.fixture
def client():
    client = create_app().test_client()
    yield client
