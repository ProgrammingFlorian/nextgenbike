from test.unit.app import client
import unittest.mock as mock
from server.app.models import User
from unittest.mock import call

users_query_all = [User(1, "Peter"), User(2, "Wei Chang"), User(3, "Florian")]
get_users_response = \
    '[{"id": 1, "username": "Peter"}, {"id": 2, "username": "Wei Chang"}, {"id": 3, "username": "Florian"}]'


@mock.patch("server.app.models.User.query.all", return_value=users_query_all)
def test_get_users(query, client):
    result = client.get("/users")
    json = result.data.decode()

    assert json == get_users_response
